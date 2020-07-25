from django.db.models import Avg

from digitalbooth.apps.authentication.models import User
from digitalbooth.apps.core.database import get_query_set, get_model_object
from digitalbooth.apps.core.models import BaseModel, models
from digitalbooth.apps.mps.models import Mps
from digitalbooth.apps.senators.models import Senators


class Vote(BaseModel):
    rate = models.IntegerField(blank=False, null=False, default=0)
    location_ip = models.GenericIPAddressField(blank=True, null=True)
    senator = models.ForeignKey(Senators, null=True, blank=True, on_delete=models.CASCADE)
    mp = models.ForeignKey(Mps, null=True, blank=True, on_delete=models.CASCADE)
    region = models.CharField(max_length=250, null=True, blank=True)
    voted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    @staticmethod
    def get_senator_votes_aggregate(senator_id):
        queryset = get_query_set(Vote)
        senator = get_model_object(Senators, 'id', senator_id)
        filtered_queryset = queryset.filter(mp__isnull=True, senator__isnull=False,
                                            senator=senator)
        return senator, filtered_queryset.aggregate(Avg('rate')).get('rate__avg')

    @staticmethod
    def get_mp_votes_aggregate(mp_id):
        queryset = get_query_set(Vote)
        mp = get_model_object(Mps, 'id', mp_id)
        filtered_queryset = queryset.filter(mp__isnull=False, senator__isnull=True,
                                            mp=mp)
        return mp, filtered_queryset.aggregate(Avg('rate')).get('rate__avg')
