{% if dockerfile and dockerfile.enabled %}
FROM {{ dockerfile.baseImageWithTag or (dockerfile.baseImage + ':' + (dockerfile.baseImageTag or 'latest')) }}

{% if dockerfile.labels %}
{% for label in dockerfile.labels %}
LABEL "{{ label.name }}"="{{ label.value }}"
{% endfor %}
{% endif %}

{% if dockerfile.user %}
USER {{ field.uid or field.user }}{% if field.gid or field.group %}:{{ field.gid or field.group }}{% endif %}
{% endif %}

{% macro F(f) %}
{% if f.onbuild %}ONBUILD {% endif %}{{ f.type }}
{%- endmacro %}

{% if dockerfile.fields %}
{% for field in dockerfile.fields %}

{% if field.type == 'ENV' %}
{{ F(field) }} "{{ field.name }}" "{{ field.value }}"
{% elif field.type == 'ADD' %}
{{ F(field) }} "{{ field.src }}" "{{ field.dest }}"
{% elif field.type == 'COPY' %}
{{ F(field) }} "{{ field.src }}" "{{ field.dest }}"
{% elif field.type == 'WORKDIR' %}
{{ F(field) }} "{{ field.path }}"
{% elif field.type == 'RUN' %}
{{ F(field) }} set -x  && {% if field.cmds %}{{ field.cmds | join(' && ') }}{% else %}{{ filed.cmd }}{% endif %}
{% endif %}

{% endfor %}
{% endif %}

{% if dockerfile.volumes is string %}
VOLUME {{ dockerfile.volumes }}
{% elif dockerfile.vomules is sequence %}
{% for volume in dockerfile.volumes %}
VOLUME {{ volume }}
{% endfor %}
{% endif %}

{% if dockerfile.ports is number or dockerfile.ports is string %}
EXPOSE {{ dockerfile.ports }}
{% elif dockerfile.ports is sequence %}
{% for port in dockerfile.ports %}
EXPOSE {{ port }}
{% endfor %}
{% endif %}

{% if dockerfile.entrypoint and dockerfile.entrypoint.cmds %}
{% if dockerfile.entrypoint.mode == 'shell' %}
ENTRYPOINT {{ dockerfile.entrypoint.cmds | join(' ') }}
{% else %}
ENTRYPOINT ["{{ dockerfile.entrypoint.cmds | join('", "') }}"]
{% endif %}
{% endif %}

{% if dockerfile.cmd and dockerfile.cmd.cmds %}
{% if dockerfile.cmd.mode == 'shell' %}
CMD {{ dockerfile.cmd.cmds | join(' ') }}
{% else %}
CMD ["{{ dockerfile.cmd.cmds | join('", "') }}"]
{% endif %}
{% endif %}

{% endif %}