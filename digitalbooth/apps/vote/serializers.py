from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from digitalbooth.apps.authentication.serializers import UserSerializer
from digitalbooth.apps.mps.serializers import MpsSerializer
from digitalbooth.apps.senators.serializers import SenatorSerializer
from digitalbooth.apps.vote.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)
    senator = SenatorSerializer(read_only=True)
    mp = MpsSerializer(read_only=True)
    rate = serializers.IntegerField(validators=[MaxValueValidator(5),
                                                MinValueValidator(0)])

    class Meta:
        model = Vote
        fields = ('id', 'rate', 'created_by', 'modified_by',
                  'location_ip', 'region', 'senator', 'mp', 'voted_by')

    def create(self, validated_data):
        senator = self.context.get('senator')
        mp = self.context.get('mp')
        voted_by = self.context.get('voted_by', None)
        location_ip = self.context.get('location_ip', None)
        region = self.context.get('region', None)
        created_by = self.context.get('created_by')
        return Vote.objects.create(created_by=created_by,
                                   senator=senator, mp=mp,
                                   region=region,
                                   voted_by=voted_by, location_ip=location_ip,
                                   **validated_data)

    def update(self, instance, validated_data):
        instance.modified_by = self.context.get('modified_by', instance.modified_by)
        instance.senator = self.context.get('senator', instance.senator)
        instance.mp = self.context.get('mp', instance.mp)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance


class IndividualVotesSerializer(serializers.Serializer):
    senator = SenatorSerializer(read_only=True)
    mp = MpsSerializer(read_only=True)
    rating = serializers.FloatField()
