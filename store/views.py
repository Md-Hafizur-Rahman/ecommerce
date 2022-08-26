from argparse import Action
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
        orders= Order.objects.filter(customer = customer, complete=False)
        #cartItems = orders.get_cart_items

        #items=order.orderitem_set.all() or we can write
        #items=order.orderitem.all()
        items=[]
        for order in orders:
            for item in order.orderitem.all():
                items.append(item)
        #cost = sum(a.get_cart_total for a in orders)
        Titem=sum(a.get_cart_item for a in orders)
    else:
        """ cartItems=orders['get_cart_items']
        print(cartItems) """
        shipping=False
        items=[]
        cost=0
        Titem=0
    products=Product.objects.all()
    context = {'products':products,'Titem':Titem}
    return render(request, 'store/store.html', context)


def cart(request):
    
    if request.user.is_authenticated:
        customer=request.user.customer
        orders= Order.objects.filter(customer = customer, complete=False)
        items=[]
        for order in orders:
            for item in order.orderitem.all():
                items.append(item)
        cost = sum(a.get_cart_total for a in orders)
        Titem=sum(a.get_cart_item for a in orders)
    else:
        shipping=False
        items=[]
        cost=0
        Titem=0
         
    context = {'items':items, 'cost': cost,'Titem':Titem}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        orders= Order.objects.filter(customer = customer, complete=False)
        items=[]
        for order in orders:
            for item in order.orderitem.all():
                items.append(item)
        cost = sum(a.get_cart_total for a in orders)
        Titem=sum(a.get_cart_item for a in orders)
        shipping = True if True in [x.shipping for x in orders] else False
    else:
        shipping=False
        items=[]
        cost=0
        Titem=0
    context ={'items':items, 'cost': cost,'Titem':Titem, 'shipping': shipping}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    Data=json.loads(request.body)
    productId=Data['productId']
    action=Data['action']
    customer=request.user.customer
    product=Product.objects.filter(id=productId).first()
    order= Order.objects.filter(customer = customer, complete=False).first()
    orderItems, create= OrderItem.objects.get_or_create(order= order, product=product)
    
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
    