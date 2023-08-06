==============
Calvo Comments 
==============
A reusable Django & Javascript app (jQuery) for simply implementing a comments feed on any url. Go here to get started: https://github.com/NYARAS/calvine-comments-application

Coming soon

Quick start
-----------
1. Install Dep:
    pip install djangorestframework django-cors-headers

2. Add "comments" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'corsheaders', # https://github.com/ottoyiu/django-cors-headers
        'rest_framework', # http://www.django-rest-framework.org/
        'comments',
    ]

