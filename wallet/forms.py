from django import forms
from .models import KarunaCurrent

class KarunaClaimForm(forms.ModelForm):
    amount = forms.IntegerField(min_value=0)
    description = forms.CharField(max_length=300,widget=forms.TextInput(attrs={"placeholder":"title"}))
    receipt = forms.ImageField()
    transaction_id = forms.CharField(max_length=30)

    class Meta:
        model = KarunaCurrent
        fields = [
            'amount',
            'description',
            'receipt',
            'transaction_id'
        ]



