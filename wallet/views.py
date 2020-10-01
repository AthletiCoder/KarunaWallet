from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import Wallet, KarunaCurrent
from .forms import KarunaClaimForm

@login_required
def profile(request, template_name="wallet/profile.html"):
    args = {}
    user = request.user
    wallet = Wallet.objects.filter(user=user)
    args['user'] = user
    args['wallet'] = wallet.first()
    return TemplateResponse(request, template_name, args)

def dashboard(request, template_name="wallet/dashboard.html"):
    args = {}
    currents = KarunaCurrent.objects.filter(wallet__user=request.user).order_by('-timestamp')
    args['currents'] = currents
    return TemplateResponse(request, template_name, args)

def karuna_claim(request, template_name="wallet/karuna_claim.html"):
    args = {}
    return TemplateResponse(request, template_name, args)

def leaderboard(request, template_name="wallet/leaderboard.html"):
    all_wallets = Wallet.objects.all().order_by('-balance')
    args = {"wallets": all_wallets}
    return TemplateResponse(request, template_name, args)