from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import Wallet, KarunaCurrent
from .forms import KarunaClaimForm, UpdateWalletForm
from django.http import HttpResponse
from django.db.utils import IntegrityError
from django.utils import timezone
from django.urls import reverse, path
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def profile(request, template_name="wallet/profile.html"):
    args = {}
    user = request.user
    wallet = Wallet.objects.filter(user=user)
    args['user'] = user
    args['wallet'] = wallet.first()
    return TemplateResponse(request, template_name, args)

@login_required
def dashboard(request, template_name="wallet/dashboard.html"):
    args = {}
    if request.user.username == 'admin':
        args["admin"] = True
        currents = KarunaCurrent.objects.filter().order_by('-timestamp')
    else:
        args["admin"] = False
        currents = KarunaCurrent.objects.filter(wallet__user=request.user).order_by('-timestamp')
    args['currents'] = currents
    return TemplateResponse(request, template_name, args)

@login_required
def karuna_claim(request, template_name="wallet/karuna_claim.html"):
    args = {}
    errors_found = False
    if request.method == "POST":
        form = KarunaClaimForm(request.POST, request.FILES)
        args["form"] = form
        if form.is_valid():
            form_data = form.cleaned_data
            clean_form = {key:value for key,value in form_data.items() if value!=""}
            wallet = Wallet.objects.filter(user=request.user)
            if wallet:
                wallet = wallet.first()
                if clean_form.get("amount") <= wallet.balance:
                    clean_form["wallet_id"] = wallet.id
                    try:
                        KarunaCurrent.objects.create(**clean_form)
                    except IntegrityError as e:
                        messages.error(request, str(e))
                        errors_found = True
                else:
                    messages.error(request, "You don't have sufficient balance to make the claim")
                    errors_found = True
            else:
                messages.error(request, "Please setup wallet first")
                errors_found = True
    form = KarunaClaimForm()
    args["form"] = form
    if request.method=="POST" and not errors_found:
        messages.info(request,"Claim submitted successfully!")
        return redirect('/dashboard')
    return TemplateResponse(request, template_name, args)

@login_required
def leaderboard(request, template_name="wallet/leaderboard.html"):
    all_wallets = Wallet.objects.all().order_by('-balance')
    args = {"wallets": all_wallets}
    return TemplateResponse(request, template_name, args)

@login_required
def update_wallet(request, template_name="wallet/update_wallet.html"):
    args = {}
    form = UpdateWalletForm()
    clean_form = None
    errors_found = False
    if request.method == "POST":
        form = UpdateWalletForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data.pop("retype_account_number")
            clean_form = {key:value for key,value in form_data.items() if value!=""}
            wallet = Wallet.objects.filter(user=request.user)
            if wallet:
                wallet.update(**clean_form)
            else:
                clean_form["user"] = request.user
                try:
                    Wallet.objects.create(**clean_form)
                except IntegrityError as e:
                    request.error(str(e))
                    errors_found = True
        if not errors_found:
            if clean_form:
                messages.info(request, "Successfully updated wallet details")
            else:
                messages.error(request, "No changes made to wallet details")
                errors_found = True
    args["form"] = form
    if request.method=="POST" and not errors_found:
        return redirect('/profile')
    return TemplateResponse(request, template_name, args)

def approve_claim(request, claim_id, transaction_type, template_name='wallet/dashboard.html'):
    errors_found = False
    if request.user.username=='admin':
        current = KarunaCurrent.objects.filter(id=claim_id)
        args = {}
        if not current:
            messages.error(request, "Invalid claim id")
            errors_found = True
        obj = current.first()
        wallet = obj.wallet
        if wallet.balance >= obj.amount:
            wallet.balance -= obj.amount
            params = {
                "transaction_status":"Approved",
                "transaction_type": transaction_type,
                "approved_timestamp": timezone.now()
            }
            current.update(**params)
        else:
            messages.error(request,"The devotee doesn't have sufficient balance, can't approve now pr")
            errors_found = True
    else:
        messages.error(request, "Only admin is allowed to approve claims")
        errors_found = True
    if request.method=="POST" and not errors_found:
        messages.info(request,"Claim submitted successfully!")
    return redirect('/dashboard')

@login_required
def delete_claim(request, claim_id):
    args = {}
    obj = KarunaCurrent.objects.filter(id=claim_id).first()
    if obj.transaction_status!="Submitted":
        messages.error(request, "Claims that have been submitted can't be deleted")
    else:
        KarunaCurrent.objects.filter(id=claim_id).delete()
        messages.info(request, "Successfully deleted claim")
    return redirect('/dashboard')