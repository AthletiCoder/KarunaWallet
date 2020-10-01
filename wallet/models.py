from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, verbose_name='Account owner', on_delete=models.CASCADE, related_name='account_owner')
    balance = models.IntegerField(verbose_name='Karuna balance', default=0)
    peak_balance = models.IntegerField(verbose_name='Peak Karuna Balance', default=balance)
    account_number = models.CharField(verbose_name='Account number', max_length=20, unique=True, null=True)
    ifsc_code = models.CharField(verbose_name='IFSC code', max_length=20, null=True)
    mobile_number = models.CharField(verbose_name='Mobile number', max_length=10, unique=True)

    def clean(self):
        if (self.account_number and not self.ifsc_code) or (self.ifsc_code and not self.account_number):
            raise ValidationError("Account number and IFSC code should be given together")
        if not self.mobile_number and not self.account_number:
            raise ValidationError("All bank details can't be empty")

class KarunaCurrent(models.Model):
    wallet = models.ForeignKey(Wallet, verbose_name="Linked wallet", on_delete=models.CASCADE, related_name='linked_wallet')
    timestamp = models.DateTimeField(verbose_name='date')
    amount = models.IntegerField(verbose_name='Amount')
    description = models.CharField(max_length=300)
    receipt = models.ImageField(verbose_name='Photo of receipt')
    transaction_id = models.CharField(max_length=30)

    class TransactionStatus(models.TextChoices):
        SUBMITTED = 'Submitted', 'Submitted'
        APPROVED = 'Approved', 'Approved'
        RECEIVED = 'Received', 'Received'
    transaction_status = models.CharField(verbose_name='Transaction status', max_length=10, choices=TransactionStatus.choices)

    class TransactionType(models.TextChoices):
        UPI = 'UPI', 'UPI'
        BANK = 'Band', 'Bank'
        CREDIT = 'Credit', 'Credit'
    transaction_type = models.CharField(verbose_name='Transaction type', max_length=10, choices=TransactionType.choices)

    def clean(self):
        if (self.transaction_type!=self.TransactionType.CREDIT) and (not self.receipt or not self.transaction_id):
            raise ValidationError("Non-credit transactions should have non-null bank details")