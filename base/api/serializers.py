from django.db import models
from django.db.models import fields
from django.db.models.expressions import Col
from base.models import NewUser, OTP
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class AccountSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email', 'id', 'password', 'name']
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

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

