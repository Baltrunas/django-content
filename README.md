# django-content
Simple django app to organize page content like flat pages with tree blocks structure.
Also, it can add extra content to any page in other apps.

## Requirements
* django-helpful
* sorl-thumbnail

## Install
* Add ```"apps.context",``` to ```INSTALLED_APPS ```
* Add ```"apps.cms.context_processors.page",``` to ```context_processors``` 
* Add ```"apps.content.middleware.PageMiddleware",``` to ```MIDDLEWARE```
* Run ```migrate content```

## Notise
If you want to use template replacement you must use
```TemplateResponse``` instead of ```render``` in you views.

If you want to use multilanguage you must install ```django-modeltranslation```, 
define LANGUAGES in settings and use ```"middleware.SwitchLocaleMiddleware",```
to change languages.

## To Do
* Update templates
* Refactor templatetags
* URLs for blocks
* PyPI
* Documentation

## Does it need?
* Tags
* Exptra meta data
* Structure for news as archive 

## Re check
- django-portfolio
- django-gallery
- django-files
