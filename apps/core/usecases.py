
from io import StringIO

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import raise_errors_on_nested_writes

from apps.core.utils import update

User = get_user_model()


class BaseUseCase:
    """
    Base Use Case
    """

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _factory(self):
        raise NotImplementedError("Subclasses should implement this!")

    def is_valid(self):
        return True


class CreateUseCase(BaseUseCase):
    def __init__(self, serializer):
        self._serializer = serializer
        self._data = self._serializer.validated_data

    def execute(self):
        self.is_valid()
        self._factory()


class UpdateUseCase(BaseUseCase):
    def __init__(self, serializer, instance):
        self._serializer = serializer
        self._data = serializer.validated_data
        self._instance = instance

    def execute(self):
        self.is_valid()
        self._factory()
        return self._instance

    def _factory(self):
        raise_errors_on_nested_writes('update', self._serializer, self._data)
        update(instance=self._instance, data=self._data)


class DeleteUseCase(BaseUseCase):

    def __init__(self, instance):
        self._instance = instance

    def execute(self):
        self.is_valid()
        self._factory()
        return self._instance

    def _factory(self):
        self._instance.delete()