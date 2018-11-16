# django-metrics
Metrics in django

## Requirements
Django 2.0+

## Usage

Add it in `middleware` in `settings.py` file

```
MIDDLEWARE = [
    ...
    'common.middleware.MetricsMiddleware'
]
```
