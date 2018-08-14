from django.urls import path
from django.conf.urls import include, url
from rest_framework_nested import routers

from sal import views

"""
Uses rest_framework_nested package to have service area as a child of a provider
"""


router = routers.SimpleRouter()
router.register(r'providers', views.ProviderViewSet, base_name='providers')

providers_router = routers.NestedSimpleRouter(
    router, r'providers', lookup='provider')
providers_router.register(
    r'serviceareas', views.ServiceAreaViewSet, base_name='provider-serviceareas')

urlpatterns = [
    path('locator/<lat>/<lng>/',
         views.ServiceAreaLocatorView.as_view(), name='locator'),
    url(r'^', include(router.urls), ),
    url(r'^', include(providers_router.urls)),
]
