from django.db import models
from django.db.models import fields
from django.db.models.expressions import Col
from base.models import NewUser, OTP
from rest_framework.serializers import ModelSerializer

class AccountSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email', 'id', 'user_name', 'password', 'name']
        # extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class OtpSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

class CheckVerify(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['is_verified']