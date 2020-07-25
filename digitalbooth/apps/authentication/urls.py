from rest_framework.routers import DefaultRouter
from django.urls import path, include

from digitalbooth.apps.authentication.views import RegistrationViewSet, LoginView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', RegistrationViewSet, basename='user')

urlpatterns = (
    path('', include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
)
