import uuid
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class Transaction(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)  # Custom TXNID-prefixed ID
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        # Ensure unique TXNID-prefixed ID
        if not self.id:
            self.id = self.generate_unique_txnid()
        super().save(*args, **kwargs)

    def generate_unique_txnid(self):
        """Generate a unique TXNID-prefixed ID"""
        while True:
            txnid = 'TXNID' + str(uuid.uuid4().hex[:12]).upper()  # Generate TXNID
            if not Transaction.objects.filter(id=txnid).exists():
                return txnid

    def __str__(self):
        return f'{self.id} - {self.name}'
