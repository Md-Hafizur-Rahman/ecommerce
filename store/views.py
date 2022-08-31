from argparse import Action
from cmath import cos
import datetime
from email.headerregistry import Address
from unicodedata import name
from venv import create
from django.shortcuts import render
from .models import *
from .utils import cookieCart,cartData

from django.http import JsonResponse
import json

def store(request):
    data=cartData(request)
    Titem=data['Titem']
    
    products=Product.objects.all()
    context = {'products':products,'Titem':Titem}
    return render(request, 'store/store.html', context)
def cart(request):
    data=cartData(request)
    Titem=data['Titem']
    order=data['order']
    items=data['items']
    context = {'items':items, 'order': order,'Titem':Titem}
    return render(request, 'store/cart.html', context)
def checkout(request):
    data=cartData(request)
    Titem=data['Titem']
    order=data['order']
    items=data['items']
    shipping=False
    context ={'items':items, 'order': order,'Titem':Titem}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    Data=json.loads(request.body)
    productId=Data['productId']
    action=Data['action']
    customer=request.user.customer
    product=Product.objects.filter(id=productId).first()
    orders,created= Order.objects.get_or_create(customer = customer, complete=False)
    orderItems, create= OrderItem.objects.get_or_create(order= orders, product=product)
    
    if action=='add':
        try:
            orderItems.quantity=(orderItems.quantity + 1)
            orderItems.save()
        except:
            pass
    elif action=='remove':
        try:
            orderItems.quantity=(orderItems.quantity-1)
            orderItems.save()
        except:
            pass
    
    if orderItems.quantity<=0:
       orderItems.delete()
    return JsonResponse('Item was added',safe=False)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def processOrder(request):
    transaction_id =datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.customer
        order = Order.objects.get(customer=customer, complete=False)
        total=float(data['form']['total'])
        order.transaction_id=transaction_id
        print("Transaction id ",order.transaction_id)
        if total==float(order.get_cart_item):
            order.complete=True
        order.save()
        
        if order.shipping:
            ShippingAddress.objects.create(
            customer=customer,
            #order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
          
    else:
        print('User is not logged in...')
        print('COOKIES:',request.COOKIES)
        name=data['form']['name']
        email=['form']['email']
        cookieData=cookieCart(request)
        items=cookieData['item']
    return JsonResponse('payment successfull!',safe=False)