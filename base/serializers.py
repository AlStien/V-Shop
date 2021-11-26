from base.models import NewUser, OTP
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class AccountSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email', 'id', 'password', 'name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CheckVerify(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['is_verified']

class OTPSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp', 'otpEmail']

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['email', 'name', 'dateOfBirth', 'gender', 'mobile', 'picture', 'address', 'is_prime', 'is_seller']
        # fields = ['name', 'dateOfBirth', 'gender', 'mobile', 'picture', 'address', 'is_seller']
        extra_kwargs = {'email': {'required': False}}

class AuthorIDSerializer(ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','name']
