import factory
from faker import Faker

from digitalbooth.apps.mps.models import Mps

fake = Faker()


class MpFactory(factory.DjangoModelFactory):
    class Meta:
        model = Mps

    name = fake.name()
    img_url = fake.url()
    county = fake.name()
    constituency = fake.name()
    party = fake.name()
    field_status = fake.name()
