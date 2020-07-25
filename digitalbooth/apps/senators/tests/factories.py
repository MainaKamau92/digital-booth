import factory
from faker import Faker

from digitalbooth.apps.senators.models import Senators

fake = Faker()


class SenatorFactory(factory.DjangoModelFactory):
    class Meta:
        model = Senators

    name = fake.name()
    img_url = fake.url()
    county = fake.name()
    party = fake.name()
    field_status = fake.name()
