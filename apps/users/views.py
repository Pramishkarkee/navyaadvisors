from rest_framework.response import Response
from apps.core import generics
from apps.core.mixins import ResponseMixin
from apps.users import serializers
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema


class LoginView(generics.CreateAPIView, ResponseMixin):
    """
    Use this end-point to get access token for normal user
    """
    throttle_scope = 'login'

    serializer_class = serializers.UserLoginSerializer
    response_serializer_class = serializers.UserLoginResponseSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        pass

    @swagger_auto_schema(responses={200: serializers.UserLoginResponseSerializer()})
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def response(self, result, serializer, status_code):
        response_serializer = self.get_response_serializer(serializer.validated_data)
        return Response(response_serializer.data, status=status_code)