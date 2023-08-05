<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-templates-variables.svg?longCache=True)](https://pypi.org/project/django-templates-variables/)

#### Installation
```bash
$ [sudo] pip install django-templates-variables
```

#### `settings.py`
```python
INSTALLED_APPS+= [
    'django_templates_variables'
]

TEMPLATES = [
    {
        # …
        'OPTIONS': {
            'context_processors': [
                'django_templates_variables.context_processors.templates_variables',
            ],
        },
    },
]
```

#### Examples
`settings.py`
```python
TEMPLATES_VARIABLES = dict(
    settings = dict(
        DEBUG=DEBUG,
        VAR="VALUE"
    )
)
```

`template.html`:
```html
{% if settings.DEBUG %}
    {{ settings.VAR }}
{% endif %}
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>