# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from rest_framework import routers
from api.views import FactorViewSet,RadiatorsViewSet,VerticalViewSet,HorizontalViewSet,FinsViewSet,DesignViewSet,EddyViewSet

urlpatterns = patterns('api.views',

    # REST API
    url(r'^$', 'root'),
    url(r'^getuserdata/$', 'get_user_data'),
    url(r'^iterators/$', 'iterators'),
)


router = routers.DefaultRouter()
router.register(r'factors', FactorViewSet)
router.register(r'radiators', RadiatorsViewSet)
router.register(r'vertical', VerticalViewSet)
router.register(r'designs', DesignViewSet)
router.register(r'horizontal', HorizontalViewSet)
router.register(r'fins', FinsViewSet)
router.register(r'eddys', EddyViewSet)
urlpatterns += router.urls