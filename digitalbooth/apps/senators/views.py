from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from digitalbooth.apps.core.database import get_model_object, get_query_set
from digitalbooth.apps.senators.models import Senators
from digitalbooth.apps.senators.renderers import SenatorJSONRenderer
from digitalbooth.apps.senators.serializers import SenatorSerializer


class SenatorsViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (SenatorJSONRenderer,)
    serializer_class = SenatorSerializer

    def create(self, request):
        senator = request.data or {}
        created_by = request.user
        serializer_context = {
            'created_by': created_by
        }
        serializer = self.serializer_class(data=senator, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        senator = request.data or {}
        instance = get_model_object(model=Senators, column_name='id', column_value=pk)
        modified_by = request.user
        serializer_context = {
            'modified_by': modified_by
        }
        serializer = self.serializer_class(data=senator, instance=instance, context=serializer_context, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = get_query_set(Senators)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        employee = get_model_object(model=Senators, column_name="id", column_value=pk)
        serializer = self.serializer_class(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        instance = get_model_object(model=Senators, column_name='id', column_value=pk)
        instance.delete()
        return Response(dict(message='Senator record deleted successfully'), status=status.HTTP_200_OK)
