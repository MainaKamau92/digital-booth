from django.db.models import Avg
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from digitalbooth.apps.core.database import get_model_object, get_query_set
from digitalbooth.apps.mps.models import Mps
from digitalbooth.apps.senators.models import Senators
from digitalbooth.apps.vote.models import Vote
from digitalbooth.apps.vote.renderers import VoteJSONRenderer
from digitalbooth.apps.vote.serializers import VoteSerializer, IndividualVotesSerializer
from digitalbooth.apps.vote.utils.user_metadata import get_ip_address


class VoteViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    renderer_classes = (VoteJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer

    def create(self, request):
        vote = request.data or {}
        location_ip, region = get_ip_address(request)
        senator_id = vote.get('senator')
        mp_id = vote.get('mp')
        if senator_id is None and mp_id is None:
            raise ValidationError('You need an mp or senator field')
        senator = get_model_object(model=Senators, column_name='id',
                                   column_value=senator_id) if senator_id is not None else None
        mp = get_model_object(model=Mps, column_name='id', column_value=mp_id) if mp_id is not None else None
        serializer_context = {
            'location_ip': location_ip,
            'region': region,
            'created_by': request.user,
            'voted_by': request.user,
            'senator' if senator is not None else None: senator,
            'mp' if mp is not None else None: mp
        }
        serializer = self.serializer_class(data=vote, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        vote = request.data
        instance = get_model_object(model=Vote, column_name='id', column_value=pk)
        senator_id = vote.get('senator')
        mp_id = vote.get('mp')
        senator = get_model_object(model=Senators, column_name='id',
                                   column_value=senator_id) if senator_id is not None else None
        mp = get_model_object(model=Mps, column_name='id', column_value=mp_id) if mp_id is not None else None
        serializer_context = {
            'created_by': request.user,
            'voted_by': request.user,
            'senator' if senator is not None else None: senator,
            'mp' if mp is not None else None: mp
        }
        serializer = self.serializer_class(data=vote, instance=instance, context=serializer_context, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def _get_aggregate(politician_id, queryset):
        return queryset.filter(id=politician_id).aggregate(Avg('rate'))

    def list(self, request):
        mps_queryset = get_query_set(Mps)
        senators_queryset = get_query_set(Senators)
        seat = request.query_params.get('seat')
        if seat == 'senate':
            page = self.paginate_queryset([{'senator': Vote().get_senator_votes_aggregate(senator_id=senator.id)[0],
                                            'rating': Vote().get_senator_votes_aggregate(senator_id=senator.id)[
                                                          1] or 0.00} for
                                           senator in
                                           senators_queryset])
            serializer = IndividualVotesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        page = self.paginate_queryset([{'mp-    ': Vote().get_mp_votes_aggregate(mp_id=mp.id)[0],
                                        'rating': Vote().get_mp_votes_aggregate(mp_id=mp.id)[
                                                      1] or 0.00} for
                                       mp in
                                       mps_queryset])
        serializer = IndividualVotesSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk):
        employee = get_model_object(model=Vote, column_name="id", column_value=pk)
        serializer = self.serializer_class(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
