from abc import ABC

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from drf_recaptcha.fields import ReCaptchaV3Field


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'phone_number']


class AuthCodeSerializer(serializers.Serializer):
    recaptcha = ReCaptchaV3Field(action="auth-code")
    phone_number = serializers.CharField(allow_null=False)

    def validate(self, attrs):
        attrs['phone_number'] = self._normalize_phone_number_or_raise(attrs['phone_number'])
        return attrs

    @staticmethod
    def _normalize_phone_number_or_raise(phone_number: str) -> str:
        if phone_number.startswith("+98"):
            normal_phone_number = phone_number
        elif phone_number.startswith("0098"):
            normal_phone_number = f"+{phone_number[2:]}"
        elif phone_number.startswith("09"):
            normal_phone_number = f"+98{phone_number[1:]}"
        elif phone_number.startswith("9"):
            normal_phone_number = f"+98{phone_number}"
        else:
            raise ValidationError("Currently, only Iran phone numbers are accepted!")
        if len(normal_phone_number) != len("+989120001122"):
            raise ValidationError("Invalid phone number!")
        return normal_phone_number

    def update(self, instance, validated_data):
        pass
        raise NotImplementedError("CodeRequestSerializer is just for deserializing data.")

    def create(self, validated_data):
        pass
        raise NotImplementedError("CodeRequestSerializer is just for deserializing data.")


class AuthCodeRequestSerializer(AuthCodeSerializer):
    pass


class AuthCodeSubmitMessageSerializer(AuthCodeSerializer):
    auth_code = serializers.CharField(allow_null=False)
