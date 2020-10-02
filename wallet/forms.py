from django import forms
from .models import KarunaCurrent, Wallet

class KarunaClaimForm(forms.Form):
    amount = forms.IntegerField(min_value=0)
    description = forms.CharField(max_length=300,widget=forms.Textarea(attrs={"placeholder":"Full description on why the claim is made","cols":60,"rows":5}))
    receipt = forms.ImageField(widget=forms.FileInput())
    transaction_id = forms.CharField(max_length=30)

class UpdateWalletForm(forms.Form):
    account_number = forms.CharField(max_length=20, required=False)
    ifsc_code = forms.CharField(max_length=20, label='IFSC Code', required=False)
    mobile_number = forms.CharField(max_length=10, label='Mobile number', required=False)

    def clean(self):
        if super().is_valid():
            if self.cleaned_data.get("mobile_number") and Wallet.objects.filter(mobile_number=self.cleaned_data.get("mobile_number")):
                raise forms.ValidationError("Wallet with same mobile number already exists")
            if self.cleaned_data.get("account_number") and Wallet.objects.filter(account_number=self.cleaned_data.get("account_number")):
                raise forms.ValidationError("Wallet with same account number already exists")