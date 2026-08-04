from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.accounts.views import AccountViewSet, RegisterView


router = DefaultRouter()

router.register(r'accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls))
]