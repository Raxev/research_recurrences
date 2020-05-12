"""djangorecurrencedemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog

# https://django-recurrence.readthedocs.io/en/latest/installation.html#install

# Your normal URLs here...
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("RecurrenceDemo.urls")),
]

js_info_dict = {
    'packages': ('recurrence', ),
}

# jsi18n can be anything you like here
urlpatterns += [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript_catalog'),
]