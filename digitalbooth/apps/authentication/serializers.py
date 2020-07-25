from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from digitalbooth.apps.authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        min_length=4,
        required=True,
        regex=r"^[a-zA-Z0-9_.-]+$",
        error_messages={
            'min_length': 'Username should be at least 4 characters long',
            'blank': 'Username cannot be blank',
            'required': 'Username is required'
        }
    )
    password = serializers.RegexField(
        regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
        min_length=8,
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={
            "regex": "Invalid password",
            "min_length": "Password should have a minimum of eight characters.",
            "required": "The password field cannot be empty."
        }
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'created_at', 'updated_at']
        read_only = ['created_at', 'updated_at']
        extra_kwargs = {
            'email': {
                'error_messages': {
                    'required': 'Email is required',
                    'blank': 'Email field cannot be empty',
                    'invalid': 'Please enter a valid email address'
                },
                'validators': [
                    UniqueValidator(queryset=User.objects.all(),
                                    message='A user with this email already exists')
                ]
            },

            'username': {
                'error_messages': {
                    'required': 'Username is required',
                    'blank': 'Username field cannot be empty'
                },
                'validators': [
                    UniqueValidator(queryset=User.objects.all(),
                                    message='A user with this username already exists')
                ]
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=300, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag to tell us whether the user has been banned
        # or otherwise deactivated. This will almost never be the case, but
        # it is worth checking for. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated. '
            )
        if not user.is_verified:
            raise serializers.ValidationError(
                'The email is yet to be verified.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return dict(email=user.email, username=user.username, token=user.token)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]
