from argparse import Action
import datetime
from email.headerregistry import Address
from venv import create
from django.shortcuts import render
from .models import *

from django.http import JsonResponse
import json

def store(request):
    products=Product.objects.all()
    # Azad is present
    if request.user.is_authenticated:
        customer=request.user.customer
        orders, created = Order.objects.get_or_create(customer=customer, complete=False)
        #cartItems = orders.get_cart_items
        items = orders.orderitem.all()
        Titem = orders.get_cart_item
        


        #items=order.orderitem_set.all() or we can write
        #items=order.orderitem.all()
        items=[]
        ''' for order in orders:
            for item in order.orderitem.all():
                items.append(item) '''
        #cost = sum(a.get_cart_total for a in orders)
        ''' Titem=sum(a.get_cart_item for a in orders) '''
    else:
        """ cartItems=orders['get_cart_items']
        print(cartItems) """
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        Titem = order['get_cart_items']
    products=Product.objects.all()
    context = {'products':products,'Titem':Titem}
    return render(request, 'store/store.html', context)


def cart(request):
    
    if request.user.is_authenticated:
        customer=request.user.customer
        orders,created= Order.objects.get_or_create(customer = customer, complete=False)
        items=[]
        items = orders.orderitem.all()
        ''' for order in orders:
            for item in order.orderitem.all():
                items.append(item) '''
        cost = orders.get_cart_total
        Titem = orders.get_cart_item
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        Titem = order['get_cart_items']
         
    context = {'items':items, 'cost': cost,'Titem':Titem}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        orders, created = Order.objects.get_or_create(customer=customer, complete=False)
        items=[]
        items = orders.orderitem.all()
        Titem = orders.get_cart_item
        ''' for order in orders:
            for item in order.orderitem.all():
                items.append(item) '''
        cost = orders.get_cart_total
        Titem=orders.get_cart_item
        shipping=False
        shipping=True if True in [orders.shipping] else False
        ''' shipping = True if True in [x.shipping for x in orders] else False '''
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        Titem = order['get_cart_items']
    context ={'items':items, 'cost': cost,'Titem':Titem,'shipping':shipping}
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
    return JsonResponse('payment successfull!',safe=False)