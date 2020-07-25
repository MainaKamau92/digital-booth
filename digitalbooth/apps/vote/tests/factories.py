import factory
from faker import Faker

from digitalbooth.apps.vote.models import Vote

fake = Faker()


class VoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vote

    approve = fake.boolean()
    comment = fake.text()
    location = fake.ipv4_public()
