---
apiVersion: {{ apiVersion }}
name: {{ name }}
tags:
{%- for tag in tags %}
  - {{ tag }}
{%- endfor %}
args:
  BASE_IMAGE: {{ args.BASE_IMAGE }}
  BASE_TAG: {{ args.BASE_TAG }}
labels:
  # Name of the image
  org.opencontainers.image.title: {{ labels['org.opencontainers.image.title'] }}
  org.opencontainers.image.description: {{ labels['org.opencontainers.image.description'] }}
  org.opencontainers.image.licenses: {{ labels['org.opencontainers.image.licenses'] }}
  org.opencontainers.image.url: {{ labels['org.opencontainers.image.url'] }}
  org.opencontainers.image.vendor: {{ labels['org.opencontainers.image.vendor'] }}
  org.opencontainers.image.version: {{ labels['org.opencontainers.image.version'] }}
  mil.dso.ironbank.image.keywords: {{ labels['mil.dso.ironbank.image.keywords'] }}
  mil.dso.ironbank.image.type: {{ labels['mil.dso.ironbank.image.type'] }}
  mil.dso.ironbank.product.name: {{ labels['mil.dso.ironbank.product.name']}}
resources:
{%- for resource in resources %}
  - url: {{ resource.url }}
    filename: {{ resource.filename }}
    validation:
      type: {{ resource.validation.type }}
      value: {{ resource.validation.value }}
{%- endfor %}

maintainers:
{%- for maintainer in maintainers %}
  - email: {{ maintainer.email }}
    name: {{ maintainer.name }}
    username: {{ maintainer.username }}
    cht_member: {{ maintainer.cht_member }}
{%- endfor %}
