"""KarunaWallet URL Configurationls
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls import url
from wallet import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('profile/', views.profile, name='profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('karuna-claim/', views.karuna_claim, name='karuna_claim'),
    path('approve-claim/<claim_id>/<transaction_type>/', views.approve_claim, name='approve_claim'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-wallet/', views.update_wallet, name='update_wallet'),
    path('delete-claim/<claim_id>/', views.delete_claim, name='delete_claim'),
    path('accounts/', include('allauth.urls')),
]