#!/usr/bin/env python
# -*- coding:utf-8 -*-

import six

import os
import sys
import uuid
import shutil
import json
import yaml
import zipfile
import subprocess
import base64
from datetime import datetime
import calendar
from collections import OrderedDict
from colorama import Fore, Back
from jinja2 import Environment, FileSystemLoader


class HtjsK8sCli(object):
    def __init__(self):
        self.args = []
        self.options = OrderedDict()
        self.is_debug = False
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.tpl_root = os.path.join(self.root, 'templates')
        self.tpl_env = Environment(loader=FileSystemLoader(self.tpl_root))
        self.tmp_root = os.path.join('/tmp', 'htjs-k8s')
        self.tmp_out_root = os.path.join(self.tmp_root, 'out')
        self.tmp_export_root = os.path.join(self.tmp_root, 'export')
        self.tmp_install_root = os.path.join(self.tmp_root, 'install')
        self.env = dict()
        self.default_cm_name = 'htjs-k8s'
        self.default_cm_namespace = 'kube-system'
        self.default_app_yaml = os.path.join(self.tpl_root, '__app__.yaml')

    def colorize_fmt(self, s, auto_reset=True):
        items = list()

        i = 0
        for j in range(len(s)):
            if s[j] in ['<', '[']:
                items.append(s[i:j])
                i = j
            elif s[j] in ['>', ']']:
                items.append(s[i:j+1])
                i = j + 1
        items.append(s[i:])

        stack = list()
        auto_reset_kinds = set()
        for k in range(len(items)):
            if items[k].startswith('<') and items[k].endswith('>'):
                kind = Fore
            elif items[k].startswith('[') and items[k].endswith(']'):
                kind = Back
            else:
                continue

            items[k] = items[k][1:-1]

            if items[k].startswith('/'):
                color = items[k][1:].strip().upper()
                try:
                    ii = stack.index(color)
                    del stack[ii]
                    if ii == 0:
                        if len(stack) > 0:
                            items[k] = getattr(kind, stack[0])
                        else:
                            items[k] = kind.RESET
                            auto_reset_kinds.remove(kind)
                    else:
                        items[k] = ''
                except ValueError:
                    pass
            else:
                color = items[k].strip().upper()
                if hasattr(kind, color):
                    items[k] = getattr(kind, color)
                    auto_reset_kinds.add(kind)
                    stack.insert(0, color)
                else:
                    items[k] = ''

        if auto_reset:
            for kind in auto_reset_kinds:
                items.append(kind.RESET)

        items = [x for x in items if x]
        s = ''.join(items)
        return s

    def info(self, s, colorize=True, quiet=False):
        if quiet:
            return
        if colorize:
            s = self.colorize_fmt(s)
        print(s)

    def debug(self, s, colorize=True, quiet=False):
        if quiet:
            return
        if self.is_debug:
            if colorize:
                s = self.colorize_fmt(s)
            print(s)

    def parse_args(self, argv=None):
        argv = argv if argv else sys.argv

        for arg in argv[1:]:  # type: six.string_types
            assert isinstance(arg, six.string_types)
            if arg.startswith('--'):
                kv = arg[2:].split('=', 1)
                if len(kv) == 2:
                    if kv[1].lower() in ['true', 'false', 'yes', 'no']:
                        self.options[kv[0]] = kv[1].lower() in ['true', 'yes']
                    else:
                        self.options[kv[0]] = kv[1]
                else:
                    self.options[kv[0]] = True
            else:
                self.args.append(arg)

        self.is_debug = self.options.get('debug', False)

        msg = list()
        for arg in self.args:
            msg.append('<CYAN>{}</CYAN>'.format(arg))
        for k, v in six.iteritems(self.options):
            if isinstance(v, bool):
                msg.append('--<CYAN>{}</CYAN>=<CYAN>{}</CYAN>'.format(k, 'true' if v else 'false'))
            else:
                msg.append('--<CYAN>{}</CYAN>=<CYAN>{}</CYAN>'.format(k, v))
        self.debug('$ {}'.format(' '.join(msg)))

    def popen(self, args):
        sp_env = os.environ.copy()
        sp_env.update(self.env)

        sp = subprocess.Popen(
            args,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=sp_env,
        )

        return sp

    def exec_cmd(self, args, fmt=None):
        sp = self.popen(args)
        sp.wait()

        if fmt == 'json':
            ret = json.loads(sp.stdout.read())
        elif fmt == 'yaml':
            ret = yaml.full_load(sp.stdout.read())
        else:
            ret = [x.decode().rstrip() for x in sp.stdout.readlines()]

        return ret

    def fetch_k8s_resources(self, args):
        resources = list()
        for line in self.exec_cmd(args):
            items = [x for x in line.split(' ') if x]
            if items[0] == 'NAMESPACE' and items[1] == 'NAME' and items[-1] == 'AGE':
                continue
            resources.append(items)
        return resources

    def fetch_k8s_resources_ex(self, namespace=None, resource=None, pvc=None, app_name=None):
        cmd_items = ['kubectl']
        if resource:
            cmd_items += ['get', resource]
        else:
            cmd_items += ['get', 'all']
        if namespace:
            cmd_items += ['-n', namespace]
        else:
            cmd_items += ['--all-namespaces']
        cmd_items += ['-l', 'htjs=true']
        if app_name:
            cmd_items += ['-l', 'htjs-app={}'.format(app_name)]

        cmd_line = ' '.join(cmd_items)

        resources = self.fetch_k8s_resources(cmd_line)

        if pvc:
            pvc_resources = self.fetch_k8s_resources_ex(namespace, 'pvc', app_name=app_name)
            for items in pvc_resources:
                items[1] = 'pvc/{}'.format(items[1])
                resources.append(items)

        return resources

    def cm_create(self, name=None, namespace=None):
        name = self.default_cm_name if name is None else name
        namespace = self.default_cm_namespace if namespace is None else namespace

        cmd_line = 'if [ -z "$(kubectl get cm -n {namespace} | grep -o "^{name} ")" ]; then kubectl create cm {name} -n {namespace}; fi'.format(
            name=name,
            namespace=namespace,
        )
        self.exec_cmd(cmd_line)

    def cm_set(self, k, v, name=None, namespace=None):
        name = self.default_cm_name if name is None else name
        namespace = self.default_cm_namespace if namespace is None else namespace

        self.cm_create(name, namespace)

        data = dict()
        data['data'] = {k: v}
        patch = json.dumps(data)

        cmd_line = 'kubectl patch cm {name} -n {namespace} --type merge -p \'{patch}\''.format(
            name=name,
            namespace=namespace,
            patch=patch,
        )
        self.exec_cmd(cmd_line)

    def cm_get(self, k, default=None, name=None, namespace=None):
        name = self.default_cm_name if name is None else name
        namespace = self.default_cm_namespace if namespace is None else namespace

        self.cm_create(name, namespace)

        cmd_line = 'kubectl get cm {name} -n {namespace} -o json'.format(
            name=name,
            namespace=namespace,
        )
        cm = self.exec_cmd(cmd_line, fmt='json')  # type: dict
        cm_data = cm.get('data', {})
        v = cm_data.get(k, default)
        return v

    def cm_del(self, k, name=None, namespace=None):
        self.cm_set(k, None, name, namespace)

    def cm_set_app(self, file):
        fmt = os.path.splitext(file)[1]
        if fmt.startswith('.'):
            fmt = fmt[1:]

        with open(file, 'rb+') as fo:
            content = fo.read()
            content_base64 = base64.b64encode(content).decode()

            if fmt == 'json':
                values = json.loads(content)
            elif fmt == 'yaml':
                values = yaml.full_load(content)
            else:
                return

        k8s = values.get('k8s', {})
        name = k8s.get('name')
        version = k8s.get('version', '0.0.1')

        k = 'apps.{}'.format(name)
        v = dict()
        v['version'] = version
        v['metadata'] = content_base64
        v['created'] = calendar.timegm(datetime.utcnow().timetuple())
        v = json.dumps(v)

        self.cm_set(k, v)

    def cm_get_app(self, name):
        try:
            info = json.loads(self.cm_get('apps.{}'.format(name), {}))
        except:
            info = None
        return info

    def cm_del_app(self, name):
        self.cm_del(k=name)

    def handle(self):
        self.parse_args()
        args = list(self.args) if self.args else ['help']
        assert isinstance(args, list) and len(args)
        options = dict(six.iteritems(self.options))

        if args[0] == 'create':
            self.do_create(name=args[1], path=options.get('path'), fmt=options.get('format'))
        elif args[0] == 'package':
            self.do_package(file=args[1], out=options.get('out'))
        elif args[0] == 'install':
            self.do_install(file=args[1], force=options.get('force', False))
        elif args[0] == 'list':
            self.do_list()
        elif args[0] == 'export':
            self.do_export(name=args[1], out=options.get('out'))
        elif args[0] == 'delete':
            self.do_delete(name=args[1], purge=options.get('purge', False))
        elif args[0] == 'version':
            self.do_version()
        else:
            self.do_help()

    def do_create(self, name, path=None, fmt='yaml'):
        self.info('<GREEN>CREATE</GREEN> : <CYAN>{}</CYAN>'.format(name))

        path = '.' if path is None else path
        if not os.path.isdir(path):
            os.makedirs(path)

        fmt = 'yaml' if fmt != 'json' else 'json'

        file = os.path.join(path, '{}.{}'.format(name, fmt))

        self.info(' + <CYAN>{}</CYAN>'.format(file))

        if fmt == 'yaml':
            shutil.copyfile(self.default_app_yaml, file)
        else:
            with open(self.default_app_yaml, 'r+') as fo:
                values = yaml.full_load(fo.read())
            with open(file, 'w+') as fo:
                fo.write(json.dumps(values))

        self.info('<GREEN>DONE.</GREEN>')

    def do_package(self, file, out=None, invoke_mode=False):
        out = self.tmp_out_root if out is None else out
        if not os.path.isdir(out):
            os.makedirs(out)

        fmt = os.path.splitext(file)[1].lower()
        fmt = fmt[1:] if fmt.startswith('.') else fmt

        with open(file, 'r+') as fo:
            content = fo.read()
            values = json.loads(content) if fmt == 'json' else yaml.full_load(content)

        k8s = values.get('k8s', {})
        name = k8s.get('name')
        version = k8s.get('version', '0.0.1')

        if not invoke_mode:
            self.info('<GREEN>PACKAGE</GREEN> : <CYAN>{}</CYAN>-<CYAN>{}</CYAN>'.format(name, version))

        tmp_dir = os.path.join('/tmp', 'htjs-k8s', '{}-{}-{}'.format(name, version, uuid.uuid4()))
        os.makedirs(tmp_dir)

        self.info(' + <CYAN>{}</CYAN>'.format(tmp_dir))

        items = [
            'namespace.yaml',
            'configmap.yaml',
            'rbac.yaml',
            'service.yaml',
            'deployment.yaml',
            'ingress.yaml',
        ]

        app_yaml = os.path.join(tmp_dir, '__app__.yaml')
        self.info('   + <CYAN>{}</CYAN>'.format(os.path.basename(app_yaml)))

        if fmt == 'json':
            with open(app_yaml, 'w+') as fo:
                fo.write(yaml.dump(values))
        else:
            shutil.copyfile(file, app_yaml)

        for item in items:
            tpl = self.tpl_env.get_template(item)
            lines = '\n'.join([line for line in tpl.render(**values).splitlines() if line.strip()])
            if lines:
                lines += '\n'
                self.info('   + <CYAN>{}</CYAN>'.format(item))
                with open(os.path.join(tmp_dir, item), 'w+') as fo:
                    fo.write(lines)

        pkg_file = os.path.join(out, '{}-{}.htjs-k8s.zip'.format(name, version))
        pkg_file = os.path.abspath(pkg_file)

        self.info(' + <CYAN>{}</CYAN>'.format(pkg_file))

        zipf = zipfile.ZipFile(pkg_file, 'w')
        for parent, dirnames, filenames in os.walk(tmp_dir):
            for filename in filenames:
                zipf.write(os.path.join(parent, filename), filename)
        zipf.close()

        if not self.is_debug:
            self.info(' - <CYAN>{}</CYAN>'.format(tmp_dir))
            shutil.rmtree(tmp_dir)

        if not invoke_mode:
            self.info('<GREEN>DONE.</GREEN>')

    def do_install(self, file, force=False):
        self.info('<GREEN>INSTALL</GREEN> : <CYAN>{}</CYAN>'.format(file))

        tmp_dir = os.path.join(self.tmp_install_root, '{}'.format(uuid.uuid4()))

        self.info(' + <CYAN>{}</CYAN>'.format(tmp_dir))
        os.makedirs(tmp_dir)

        if os.path.isdir(file):
            shutil.copytree(file, tmp_dir)
        else:
            try:
                zipf = zipfile.ZipFile(file)
                zipf.extractall(path=tmp_dir)
                zipf.close()
            except Exception as e:
                pass

        app_yaml = os.path.join(tmp_dir, '__app__.yaml')

        with open(app_yaml, 'r+') as fo:
            values = yaml.full_load(fo.read())

        k8s = values.get('k8s', {})
        name = k8s.get('name')
        version = k8s.get('version', '0.0.1')

        app_list = self.do_list(name=name, quiet=True)
        if app_list:
            if not force:
                self.info(' - <CYAN>{}</CYAN>'.format(tmp_dir))
                shutil.rmtree(tmp_dir)
                self.info('<RED>FILED, <MAGENTA>{}</MAGENTA><WHITE>-</WHITE><MAGENTA>{}</MAGENTA> ALREADY INSTALLED.</RED>'.format(
                    name,
                    app_list[name]['VERSION'])
                )
                return

        cmd_lines = list()

        items = [
            'namespace.yaml',
            'configmap.yaml',
            'rbac.yaml',
            'service.yaml',
            'deployment.yaml',
            'ingress.yaml',
        ]
        for item in items:
            k8s_file = os.path.join(tmp_dir, item)
            if os.path.isfile(k8s_file):
                self.info('   + <CYAN>{}</CYAN>'.format(item))
                cmd_line = 'kubectl apply -f "{}"'.format(os.path.abspath(k8s_file))
                cmd_lines.append(cmd_line)

        for cmd_line in cmd_lines:
            self.info(' $ <MAGENTA>{}</MAGENTA>'.format(cmd_line))
            self.exec_cmd(cmd_line)

        self.cm_set_app(app_yaml)

        self.info(' - <CYAN>{}</CYAN>'.format(tmp_dir))
        shutil.rmtree(tmp_dir)

        self.info('<GREEN>DONE.</GREEN>')

    def do_list(self, name=None, namespace=None, quiet=False):
        resources = self.fetch_k8s_resources_ex(namespace=namespace, pvc=True, app_name=name)

        app_list = OrderedDict()

        headers = ['NAME', 'VERSION', 'NAMESPACE', 'SERVICE', 'DEPLOYMENT', 'PVC']
        maxlen_table = dict()

        for items in resources:
            info = self.exec_cmd('kubectl get {} -n {} -o json'.format(items[1], items[0]), fmt='json')
            labels = info.get('metadata', {}).get('labels', {})

            name = labels.get('htjs-app')
            version = labels.get('htjs-app-version')

            if name not in app_list:
                app_list[name] = {
                    'NAME': name,
                    'NAMESPACE': items[0],
                    'VERSION': version,
                    'DEPLOYMENT': '-',
                    'SERVICE': '-',
                    'PVC': '-',
                }

            if items[1].startswith('service/'):
                app_list[name]['SERVICE'] = items[5]
            elif items[1].startswith('deployment.apps/') or items[1].startswith('statefulset.apps/'):
                app_list[name]['DEPLOYMENT'] = items[2]
            elif items[1].startswith('pvc/'):
                app_list[name]['PVC'] = '{}:{}({})'.format(items[6], items[4], items[2])

            for header in headers:
                maxlen_table[header] = max(maxlen_table.get(header, len(header)), len(app_list[name].get(header, '-')))

        if len(app_list):
            self.info('', quiet=quiet)

            header_line = list()
            for header in headers:
                header_line += [header + ' ' * (maxlen_table[header] - len(header))]
            header_line = '  '.join(header_line)
            self.info(header_line, quiet=quiet)

            app_index = 0
            for _, app_info in six.iteritems(app_list):
                app_line = list()
                for header in headers:
                    v = app_info.get(header, '')
                    app_line += [v + ' ' * (maxlen_table[header] - len(v))]
                app_line = '  '.join(app_line)

                app_index += 1
                if app_index % 2:
                    self.info('<CYAN>{}</CYAN>'.format(app_line), quiet=quiet)
                else:
                    self.info('<MAGENTA>{}</MAGENTA>'.format(app_line), quiet=quiet)

            self.info('', quiet=quiet)
        else:
            self.info('<YELLOW>NOT FOUND.</YELLOW>', quiet=quiet)

        return app_list

    def do_export(self, name, out=None):
        self.info('<GREEN>EXPORT</GREEN> : <CYAN>{}</CYAN>'.format(name))

        out = self.tmp_export_root if out is None else out

        info = self.cm_get_app(name)

        if isinstance(info, dict) and info:
            metadata = info.get('metadata')
            try:
                content = base64.b64decode(metadata).decode()
                self.info('')
                self.info('<MAGENTA>{}</MAGENTA>'.format(content))
                self.info('')

                tmp_dir = os.path.join(self.tmp_export_root, '{}-{}'.format(name, uuid.uuid4()))
                self.info(' + <CYAN>{}</CYAN>'.format(tmp_dir))
                os.makedirs(tmp_dir)

                app_yaml = '__app__.yaml'
                self.info('   + <CYAN>{}</CYAN>'.format(app_yaml))
                app_yaml = os.path.join(tmp_dir, app_yaml)
                with open(app_yaml, 'w+') as fo:
                    fo.write(content)

                self.do_package(app_yaml, out=out, invoke_mode=True)

                self.info(' - <CYAN>{}</CYAN>'.format(tmp_dir))
                shutil.rmtree(tmp_dir)

                self.info('<GREEN>DONE.</GREEN>')
            except:
                self.info('<RED>FAILED, INVALID METADATA.</RED>')
        else:
            self.info('<RED>FAILED, NOT FOUND.</RED>')

    def do_delete(self, name, purge=False):
        self.info('<GREEN>DELETE</GREEN> : <CYAN>{}</CYAN>'.format(name))

        resources = self.fetch_k8s_resources('kubectl get all --all-namespaces -l htjs=true -l htjs-app={}'.format(name))

        if purge:
            pvc_resources = self.fetch_k8s_resources('kubectl get pvc --all-namespaces -l htjs=true -l htjs-app={}'.format(name))
            for res in pvc_resources:
                res[1] = 'pvc/{}'.format(res[1])
                resources.append(res)

        for res in resources:
            cmd_line = 'kubectl delete {} -n {}'.format(res[1], res[0])
            self.info(' $ <MAGENTA>{}</MAGENTA>'.format(cmd_line))
            self.exec_cmd(cmd_line)

        if not self.do_list(name=name, quiet=True):
            self.cm_del_app(name)

        if len(resources):
            self.info('<GREEN>DONE.</GREEN>')
        else:
            self.info('<YELLOW>NOT FOUNT.</YELLOW>')

    def do_version(self):
        self.info('<GREEN>VERSION</GREEN> : <CYAN>0.0.2</CYAN>')

    def do_help(self):
        self.info('')
        self.info('<GREEN>OPTIONS</GREEN> : ')
        self.info('')
        self.info('  <CYAN>create         创建一个新应用的配置文件</CYAN>')
        self.info('')
        self.info('    create demo')
        self.info('    create demo --out=/tmp/')
        self.info('')
        self.info('  <CYAN>package        从指定配置文件打包一个应用</CYAN>')
        self.info('')
        self.info('    package /tmp/demo.yaml')
        self.info('    package /tmp/demo.yaml --out=/tmp/')
        self.info('')
        self.info('  <CYAN>list           列举出当前k8s中已安装的所有应用</CYAN>')
        self.info('')
        self.info('    list')
        self.info('')
        self.info('  <CYAN>export         从当前k8s中导出指定应用</CYAN>')
        self.info('')
        self.info('    export demo')
        self.info('')
        self.info('  <CYAN>delete         从当前k8s中删除指定应用</CYAN>')
        self.info('')
        self.info('    delete demo')
        self.info('    delete demo --purge')
        self.info('')
        self.info('  <CYAN>version        查看版本信息</CYAN>')
        self.info('')
        self.info('    version')
        self.info('')
        self.info('<GREEN>USAGE</GREEN> :')
        self.info('')
        self.info('  <CYAN>htjs-k8s [[]options[]]</CYAN>')
        self.info('')


def main():
    cli = HtjsK8sCli()
    cli.handle()


if __name__ == '__main__':
    main()
