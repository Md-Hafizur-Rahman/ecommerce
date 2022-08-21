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
        items=[]
        for order in orders:
            for item in order.orderitem.all():
                items.append(item)
        cost = sum(a.get_cart_total for a in orders)
        Titem=sum(a.get_cart_item for a in orders)
        cartItems=orders.get_cart_items
    else:
        cartItems=orders['get_cart_items']
        print(cartItems)
        items=[]
        cost=0
        Titem=0
        
    context = {'products':products}
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
    else:
        items=[]
        cost=0
        Titem=0
    context ={'items':items, 'cost': cost,'Titem':Titem}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    Data=json.loads(request.body)
    productId=Data['productId']
    action=Data['action']
    print('Action:', action)
    print('ProductId:', productId)
    
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    orders= Order.objects.filter(customer = customer, complete=False)
    orderItem,create=OrderItem.objects.filter(order = orders, product=product)
    
    if action=='add':
        orderItem.quantity=(orderItem.quantity + 1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
    orderItem.save()
    
    if orderItem.quantity<=0:
       orderItem.delete() 
        
    return JsonResponse('Item was added',safe=False)
    