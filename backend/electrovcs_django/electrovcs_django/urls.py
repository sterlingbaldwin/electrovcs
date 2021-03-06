"""electrovcs_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from viz.views import viz_list, viz_new, viz_run, login, viz_get, viz_save

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^django-pam/', include('django_pam.urls')),
    url(r'^viz/list/', viz_list),
    url(r'^viz/new/', viz_new),
    url(r'^viz/run/', viz_run),
    url(r'^viz/get/', viz_get),
    url(r'^viz/save/', viz_save),
    url(r'login/', login)
]

