from django.urls import path, include
from rest_framework.routers import DefaultRouter
from digitalbooth.apps.vote.views import VoteViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'votes', VoteViewSet, basename='votes')

urlpatterns = (
    path('', include(router.urls)),
)
