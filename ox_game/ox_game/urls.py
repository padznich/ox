"""ox_game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from db_mysql.views import players_listing
from db_mysql.views import log_game_events_listing
from db_mysql.views import home
from db_mysql.views import change_xp
from db_mysql.views import log_filter_by_id
from db_mysql.views import log_filter_by_date_created

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', home),
    url(r'^list/', players_listing),
    url(r'^log_list/', log_game_events_listing),
    url(r'^log_list_id/([0-9])+/', log_filter_by_id),
    url(r'^log_list_date/', log_filter_by_date_created),
    url(r'^change_xp/([0-9]+)/', change_xp),
]
