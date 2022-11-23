# django-content

## Requirements
- django-helpful
- sorl-thumbnail

## Install
* Add ```"apps.context",``` to ```INSTALLED_APPS ```
* Add ```"apps.cms.context_processors.page",``` to ```context_processors``` 
* Add ```"apps.content.middleware.PageMiddleware",``` to ```MIDDLEWARE```
* Add ```path(""", include("apps.content.urls")),``` to end of main urls.py
* Run ```migrate content```

## Notise
If you want to use multilanguage you must install ```django-modeltranslation```, 
define LANGUAGES in settings and use ```"middleware.SwitchLocaleMiddleware",```
to change languages.

## To Do
* PyPI
* Tags?
* Translate image field?
* Auto Sitemap
* Documentation
* Exptra meta data

## Thing about
* New **news** urls
	/news/some-thing-heppen/
	/news/page-1/
		http://ux.stackexchange.com/questions/16045/pagination-urls
		http://www.ayima.com/seo-knowledge/conquering-pagination-guide.html
	/news/2013/
	/news/2013/01/
	/news/2013/01/23/

=======
+ django-portfolio
+ django-gallery
+ django-files


- django-seo
- django-banners
- django-menu

-----