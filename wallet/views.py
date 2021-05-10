from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import Wallet, KarunaCurrent
from .forms import KarunaClaimForm, UpdateWalletForm, KarunaCreditForm, ReimburseClaimForm
from django.db.utils import IntegrityError
from django.utils import timezone
from django.shortcuts import redirect
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
                    clean_form["transaction_id"] = "credit"
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
        if not current:
            messages.error(request, "Invalid claim id")
            errors_found = True
        obj = current.first()
        wallet = obj.wallet
        if wallet.balance >= obj.amount:
            wallet.balance -= obj.amount
            wallet.save()
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
    obj = KarunaCurrent.objects.filter(id=claim_id).first()
    if obj.transaction_status!="Submitted":
        messages.error(request, "Claims that have been submitted can't be deleted")
    else:
        KarunaCurrent.objects.filter(id=claim_id).delete()
        messages.info(request, "Successfully deleted claim")
    return redirect('/dashboard')

@login_required
def karuna_credit(request, template_name='wallet/karuna_credit.html'):
    args = {}
    errors_found = False
    form = KarunaCreditForm()
    clean_form = None
    errors_found = False
    if request.method == "POST":
        form = KarunaCreditForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            clean_form = {key:value for key,value in form_data.items() if value!="" or value!=None}
            wallet = Wallet.objects.filter(user__username=clean_form.get("user"))
            if wallet:
                wallet_params = {}
                wallet_params["balance"] = wallet[0].balance+clean_form.get("amount")
                wallet_params["karuna_tally"] = wallet[0].karuna_tally+clean_form.get("amount")
                wallet.update(**wallet_params)

                clean_form["wallet"] = wallet.first()
                clean_form["transaction_status"] = "Received"
                clean_form["transaction_type"] = "Credit"
                clean_form.pop("user")
                try:
                    KarunaCurrent.objects.create(**clean_form)
                except IntegrityError as e:
                    messages.error(request, str(e))
                    errors_found = True
            else:
                messages.error(request, "Hare Krsna prabhu, please ask the recipient devotee to setup wallet first.")
                errors_found = True
        if not errors_found:
            if clean_form:
                messages.info(request, "Successfully deposited karuna credit")
            else:
                messages.error(request, "Failed to deposit karuna credit")
                errors_found = True
    args["form"] = form
    if request.method=="POST" and not errors_found:
        return redirect('/dashboard')
    return TemplateResponse(request, template_name, args)

@login_required
def received(request, claim_id, template_name="wallet/dashboard.html"):
    claim = KarunaCurrent.objects.filter(id=claim_id)    
    if claim:
        claim.update(**{"transaction_status":"Received"})
        messages.info(request, "Successfully acknowledged receipt")
    else:
        messages.error(request, "Invalid claim info")
    return redirect('/dashboard')


def reimburse_claim(request, claim_id, template_name='wallet/karuna_reimburse.html'):
    args = {}
    form = ReimburseClaimForm()
    clean_form = None
    errors_found = False
    if request.method == "POST":
        form = ReimburseClaimForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            clean_form = {key:value for key,value in form_data.items() if value!=""}
            clean_form["transaction_status"] = "Approved"
            if request.user.username=='admin':
                current = KarunaCurrent.objects.filter(id=claim_id)
                if not current:
                    messages.error(request, "Invalid claim id")
                    errors_found = True
                else:
                    obj = current.first()
                    wallet = obj.wallet
                    if wallet.balance >= obj.amount:
                        wallet.balance -= obj.amount
                        wallet.save()
                        clean_form["approved_timestamp"] = timezone.now()
                        try:
                            KarunaCurrent.objects.filter(id=claim_id).update(**clean_form)
                        except IntegrityError as e:
                            messages.error(request, str(e))
                            errors_found = True
                    else:
                        messages.error(request,"The devotee doesn't have sufficient balance, can't approve now pr")
                        errors_found = True
            else:
                messages.error(request,"Only admin can access this url")
                errors_found = True
    args["form"] = form
    if request.method=="POST" and not errors_found:
        return redirect('/dashboard')
    return TemplateResponse(request, template_name, args)