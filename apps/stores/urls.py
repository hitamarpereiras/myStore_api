from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.stores.views import StoreViewSet


router = DefaultRouter()

router.register('stores', StoreViewSet)

urlpatterns = [
    path('', include(router.urls))
]