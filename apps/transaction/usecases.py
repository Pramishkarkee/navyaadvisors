from apps.transaction.models import Transaction
from apps.core.usecases import BaseUseCase


class AddTransactionUseCase(BaseUseCase):
    def __init__(self,serializer):
        self.serializer = serializer
        self.data = serializer.validated_data

    def execute(self):
        self._factory()

    def _factory(self):
        self._tran = Transaction(**self.data)
        self._tran.save()

class ListTransactionUseCase(BaseUseCase):
    def execute(self):
        self._factory()
        return self._blogs

    def _factory(self):
        self._blogs = Transaction.objects.all()