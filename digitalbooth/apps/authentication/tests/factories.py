from faker import Faker
import factory

from digitalbooth.apps.authentication.models import User

fake = Faker()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: "user_%d" % x)
    email = factory.Sequence(lambda x: "user%d@digitalbooth.com" % x)
    password = factory.PostGenerationMethodCall('set_password',
                                                fake.password(length=10, special_chars=True,
                                                              digits=True, upper_case=True,
                                                              lower_case=True))
