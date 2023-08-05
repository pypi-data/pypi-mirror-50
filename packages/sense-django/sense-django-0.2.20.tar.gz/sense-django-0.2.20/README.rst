============
sense-django
============

sense-django is a simple Django app. It contains three middlewares used in django project.  

Quick start
-----------

1. Add "sense_django" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'sense_django',
    ]

2. Add "sense_django.middleware.UserTokenCheck" to your MIDDLEWARE settings like this::

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
    'sense_django.middleware.UserTokenCheck',
    'sense_django.middleware.PermissionCheck',
    'sense_django.middleware.RequestLogMiddleware'
    ]


In project, if error we have not catch，front page will show error detail and error path, no json result,so sense_django
contains a decorator to catch this error json detail

Quick start
-----------

1.Import and Add decorator in interface like this::

    from sense_django import *
    @catch_view_exception
    def test1(request):
        ...

2.In the production environment，set debug=0，in the test, set debug=1::

    settings.ini
    [settings]
    debug=0/1

