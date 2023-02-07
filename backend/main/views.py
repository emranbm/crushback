import logging
import random

from django.conf import settings
from django.core.cache import caches
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from main import utils
from main.models import User
from main.serializers import UserSerializer, AuthCodeRequestSerializer, \
    AuthCodeSubmitMessageSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=False, url_path="request-code", permission_classes=[])
    def request_code(self, request, *args, **kwargs):
        serializer = AuthCodeRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        auth_code = str(random.randrange(10_000, 100_000))
        utils.send_sms(serializer.data['phone_number'], f"DJANGO_REACT_TEMPLATE login code:\n{auth_code}")
        caches[settings.CACHE_NAME_AUTH_CODES].set(serializer.data['phone_number'], auth_code)
        return Response(status=HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=False, url_path="submit-code", permission_classes=[])
    def submit_code(self, request, *args, **kwargs):
        serializer = AuthCodeSubmitMessageSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        received_auth_code = serializer.data['auth_code']
        actual_auth_code = caches[settings.CACHE_NAME_AUTH_CODES].get(serializer.data['phone_number'])
        logging.debug(f"Phone number ({serializer.data['phone_number']}) auth code:"
                      f" Received={received_auth_code} Actual={actual_auth_code}")
        if received_auth_code != actual_auth_code:
            raise ValidationError("Invalid auth code!", code=HTTP_400_BAD_REQUEST)
        user, user_newly_created = User.objects.get_or_create(phone_number=serializer.data['phone_number'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_201_CREATED if user_newly_created else HTTP_200_OK)

    @action(methods=['GET', 'PUT', 'DELETE'], detail=False, url_path="self")
    def self_user_endpoint(self, request, *args, **kwargs):
        if request.method == "GET":
            return self._get_current_user(request, *args, **kwargs)
        elif request.method == "PUT":
            return self._update_current_user(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self._delete_current_user(request, *args, **kwargs)
        else:
            raise ValueError(f"Unexpected method: {request.method}")

    @staticmethod
    def _get_current_user(request, *args, **kwargs):
        serializer = UserSerializer(instance=request.user, context={"request": request})
        return Response(serializer.data)

    @staticmethod
    def _update_current_user(request, *args, **kwargs):
        user_serializer = UserSerializer(request.user, request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(status=HTTP_200_OK)

    @staticmethod
    def _delete_current_user(request, *args, **kwargs):
        request.user.delete()
        return Response(status=HTTP_200_OK)
