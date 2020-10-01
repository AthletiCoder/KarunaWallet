"""KarunaWallet URL Configurationls
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from wallet.views import profile, dashboard, karuna_claim, leaderboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', profile),
    path('leaderboard/', leaderboard),
    path('karuna-claim/', karuna_claim),
    path('dashboard/', dashboard),
    path('accounts/', include('allauth.urls')),
]