from django.contrib import admin

# Register your models here.
from wallet.models import Wallet, KarunaCurrent 
admin.site.register(Wallet)
admin.site.register(KarunaCurrent)