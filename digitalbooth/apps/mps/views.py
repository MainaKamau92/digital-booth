from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from digitalbooth.apps.core.database import get_model_object, get_query_set
from digitalbooth.apps.mps.models import Mps
from digitalbooth.apps.mps.renderers import MPsJSONRenderer
from digitalbooth.apps.mps.serializers import MpsSerializer


class MpsViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    renderer_classes = (MPsJSONRenderer,)
    serializer_class = MpsSerializer

    def create(self, request):
        mp = request.data or {}
        created_by = request.user
        serializer_context = {
            'created_by': created_by
        }
        serializer = self.serializer_class(data=mp, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        mp = request.data or {}
        modified_by = request.user
        instance = get_model_object(model=Mps, column_name='id', column_value=pk)
        serializer_context = {
            'modified_by': modified_by
        }
        serializer = self.serializer_class(data=mp, instance=instance, context=serializer_context, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = get_query_set(Mps)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        employee = get_model_object(model=Mps, column_name="id", column_value=pk)
        serializer = self.serializer_class(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        instance = get_model_object(model=Mps, column_name='id', column_value=pk)
        instance.delete()
        return Response(dict(message='MP record deleted successfully'), status=status.HTTP_200_OK)
