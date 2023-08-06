# django-prodperfect
Django template tags for the ProdPerfect tracking snippet.


## Installation
1. `pip install django-prodperfect`
2. Add to `INSTALLED_APPS` in your `settings.py`
    
    `prodperfect,`
3. In your templates, load `prodperfect`

## Example template
```djangotemplate
{% load prodperfect %}


<body>
    ...
    {% tracking_snippet %}
</body>
```

## Example settings.py
You can copy these values from the ProdPerfect provided tracking snippet.
```python
PRODPERFECT = {
    'HOST': 'prodperfect.datapipe.prodperfect.com/v1',
    'WRITE_KEY': '12345',
    'PROJECT_ID': '12345',
    'TRACKING_LIBRARY_URL': 'https://prodperfect.trackinglibrary.prodperfect.com/keen-tracking.min.js'
}
```

To override the default tracking behavior, you can change the value of the following properties.
```python
PRODPERFECT = {
    # ...
    'OPTIONS': {
        'ignoreDisabledFormFields': False,
        'recordClicks': True,
        'recordFormSubmits': True,
        'recordInputChanges': True,
        'recordPageViews': True,
        'recordPageUnloads': True,
        'recordScrollState': True
    }
}

```


## Bugs and suggestions

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/prodperfect/django-prodperfect/issues


## Author
Developed and maintained by [prodperfect](https://prodperfect.com/).