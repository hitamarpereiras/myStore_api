from rest_framework.routers import DefaultRouter
from apps.categories.views import CategoryViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]