from apps.transaction.models import Transaction
from rest_framework import serializers


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Transaction

class TransactionInputSerializers(serializers.ModelSerializer):
    class Meta:
        fields = ['name','email','phone','amount']
        model = Transaction
