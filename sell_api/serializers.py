import traceback
from rest_framework.utils import model_meta
from rest_framework.serializers import raise_errors_on_nested_writes
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer

from sell_api.models import Category, Item, Users

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'description', 'parent',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create_user(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    users = UsersSerializer(many=True)

    class Meta:
        model = Item
        fields = ('title', 'users', 'category', 'description', 'price', 'photo', 'time_added',)


class CustomJWTSerializer(JSONWebTokenSerializer):
    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = Users.objects.filter(username=attrs.get("username")).first()
        if user_obj is not None:
            credentials = {
                self.username_field: attrs.get(self.username_field),
                "password": password,
            }
            if all(credentials.values()):
                try:
                    user = Users.objects.get(
                        username__iexact=credentials[self.username_field]
                    )
                    if not user.is_active:
                        msg = "Users account is disabled."
                        raise serializers.ValidationError(msg)
                except Users.DoesNotExist:
                    pass

                user = authenticate(**credentials)
                if user:
                    payload = jwt_payload_handler(user)

                    return {"token": jwt_encode_handler(payload), "user": user}
                else:
                    msg = "Unable to log in with provided credentials."
                    raise serializers.ValidationError(msg)

            else:
                msg = f'Must include "{self.username_field}" and "password".'
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = "Account with this email/username does not exists"
            raise serializers.ValidationError(msg)
