import re
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext as _
from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    PasswordField
)
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.cache import LoginCache


User = get_user_model()


class CustomTokenObtainSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        cache_results = LoginCache.get(attrs['username'])
        lockout_timestamp = None
        invalid_attempt_timestamps = cache_results['invalid_attempt_timestamps'] if cache_results else []

        invalid_attempt_timestamps = [timestamp for timestamp in invalid_attempt_timestamps if
                                      timestamp > (datetime.now() - timedelta(minutes=15))]

        if len(invalid_attempt_timestamps) >= 5:
            raise serializers.ValidationError(
                _('too many attempts, account locked ! wait for 15 minutes'),
            )

        self.user = self.authenticate(username=attrs['username'], password=attrs['password'])
        if self.user is None:
            invalid_attempt_timestamps.append(datetime.now())
            if len(invalid_attempt_timestamps) >= 5:
                lockout_timestamp = datetime.now()
                raise serializers.ValidationError(
                    _('locked.')
                )
            LoginCache.set(attrs['username'], invalid_attempt_timestamps, lockout_timestamp)
            raise serializers.ValidationError(
                _('Email or Password does not matched .'),
            )
        if self.user:
            if not self.user.is_active:
                msg = _('User account is not activated.')
                raise PermissionDenied(msg)

            if self.user.is_archived:
                msg = _('User is archived.')
                raise PermissionDenied(msg)
        LoginCache.delete(attrs['username'])
        return {}

    @staticmethod
    def authenticate(username, password):
        try:
            user = User.objects.get(
                Q(email=username) | Q(username=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            User().set_password(password)


class LoginSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        self.validate_user()
        refresh = self.get_token(self.user)

        data['refresh_token'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data['role'] = "owner"
        data['color']=""
        data['id']=str(self.user.id)
        self.user.last_login = now()
        self.user.save()
        return data

    def validate_user(self):
        pass


class UserLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        data = super(UserLoginSerializer, self).validate(attrs)
        # user detail
        data['user'] = self.user

        return data


class UserLoginResponseSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    role = serializers.CharField()
    id = serializers.CharField()