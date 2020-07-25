from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from digitalbooth.apps.authentication.models import User
from digitalbooth.apps.authentication.renderers import UserJSONRenderer
from digitalbooth.apps.authentication.serializers import RegistrationSerializer, LoginSerializer


class RegistrationViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        user = request.data or {}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        if not request.user.is_authenticated:
            raise ValidationError("Authentication credentials were not provided.")
        queryset = User.objects.filter(tenant_schema=request.user.tenant_schema).all()
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data or {}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
