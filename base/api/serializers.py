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

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email is None:
            raise serializers.ValidationError('Email is required')
        if password is None:
            raise serializers.ValidationError('Password is required')

        user = authenticate(email=email, password=password)

        # user with provided credentials  not found
        if user is None:
            raise serializers.ValidationError('User with provided credentials not found')
        
        # check if user is_active
        if user.is_active!=True:
            raise serializers.ValidationError("User is deactivated")

        return {
            'email':user.email,
            'username':user.username,
            'token':user.token
        }
