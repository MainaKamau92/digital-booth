from rest_framework import serializers
from digitalbooth.apps.authentication.serializers import UserSerializer
from digitalbooth.apps.mps.models import Mps


class MpsSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    modified_by = UserSerializer(read_only=True)

    class Meta:
        model = Mps
        fields = ('id', 'name',
                  'img_url',
                  'county',
                  'constituency',
                  'party',
                  'field_status', 'created_by', 'modified_by')

    def create(self, validated_data):
        created_by = self.context.get('created_by')
        return Mps.objects.create(created_by=created_by, **validated_data)

    def update(self, instance, validated_data):
        instance.modified_by = self.context.get('modified_by', instance.modified_by)
        instance.name = validated_data.get('name', instance.name)
        instance.img_url = validated_data.get('img_url', instance.img_url)
        instance.county = validated_data.get('county', instance.county)
        instance.constituency = validated_data.get('constituency', instance.constituency)
        instance.party = validated_data.get('party', instance.party)
        instance.field_status = validated_data.get('field_status', instance.field_status)
        instance.save()
        return instance
