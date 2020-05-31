import stripe
import string
import sys
import random
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from .models import clients,transaction,paytm_Transaction,product,shipping,product_details
from django.conf import settings # new
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum
from django import template
from secapp import models

register = template.Library()

stripe.api_key = settings.STRIPE_SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context
class variables:
    name='abc'
    desc='bcd'

    def charge(request):
        charge = stripe.Charge.create(
            amount=int(str(infinity.subtotal)+'.00'),
            currency='inr',
            description='',
            source=request.POST['stripeToken']
        )
        status=charge
        if status['failure_code'] == None:
            a=transaction(email=status['billing_details']['name'],amount=status['amount'],payment_detail=status['outcome']['seller_message'])
            a.save()
            return JsonResponse(status['outcome']['seller_message'],safe=False)
        else:
            return JsonResponse(['failure_message'],safe=False)


class infinity:
    prods=['a',]
    prod_img=''
    name='a'
    subtotal=0
    dict={}
    i=0
    def bms(request):

        if request.method == 'POST':
            infinity.name=request.POST['user']
            passwod=request.POST['pass']
            obj=clients.objects.all()
            len_obj=len(list(clients.objects.all()))
            for i in range(len_obj):
                if infinity.name==obj[i].user_name and passwod==obj[i].password:
                    prod=list(product.objects.all())
                    infinity.prods=prod
            return render(request,'infinity.html',{'prods':infinity.prods})
            
        else:
            return render(request,'login.html') 

    def cart(request):
        
        p=product.objects.all()
        global prod
        prod=product_details()
        print(request.POST.getlist('products'))
        (infinity.dict).clear()
        infinity.subtotal=0
        
        for k in range(len(list(p))):
            
            if p[k].productName in request.POST.getlist('products'):
                e=(p[k].productName).split()
                quantity=int(request.POST[e[0]])
                total=p[k].productPrice * quantity
               
                infinity.dict[k]={k:{'Name':p[k].productName,'Img':p[k].productImg,'Price':p[k].productPrice,'quantity':quantity,'total':total}}
                
                print(request.POST.getlist('products'))
                infinity.subtotal=infinity.subtotal+total
                infinity.i=+1
        print(infinity.dict)        
        return render(request,'cart.html',{'dict':infinity.dict,'subtotal':infinity.subtotal})

    
    def hel(request):
        global ship
        ship=shipping()
        ship.country=request.POST['country']
        ship.state=request.POST['state']
        ship.pincode=request.POST['pincode']
        return render(request,'hel.html',{'amount':infinity.subtotal})
    
    def initiate_payment(request):
        if request.method == "GET":
            return render(request, 'paytm_login.html')
    
        paytm_transaction = paytm_Transaction.objects.create(made_by=infinity.name, amount=infinity.subtotal)
    #paytm_transaction.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        N=7
        res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(res)),
            ('CUST_ID', str(paytm_transaction.made_by)),
        #('CUST_ID', str(paytm_transaction.made_by.email))
            ('TXN_AMOUNT', str(paytm_transaction.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)
        paytm_transaction.checksum = checksum
    #paytm_transaction.save()

        paytm_params['CHECKSUMHASH'] = checksum
        print('SENT: ', checksum)
        return render(request, 'paytm_redirect.html', context=paytm_params)

def pays(request):
    if request.GET['payments'] == 'credit':
        return render(request,'newe.html')
    elif request.GET['payments'] == 'ptm':
        return render(request,'newf.html')
    elif request.GET['payments'] == 'gpay':
        return render(request,'gpay.html')



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
            return render(request, 'confirmation.html',{'shipping':ship,'context':received_data,'dict':infinity.dict,'amount':infinity.subtotal})
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'paytm_callback.html', context=received_data)

def checkbox(request):
    if request.method=='POST':
       # m=request.POST['vehicle']
        print(request.POST.getlist('vehicle'))
        return render(request,'checkbox.html',{'m':request.POST['vehicle']})
    else:
        return render(request,'checkbox.html')
    
# Create your views here.
