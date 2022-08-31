import json
from .models import *

def cookieCart(request):
        try:
            cart=json.loads(request.COOKIES['cart'])
        except:
            cart={}
        print('cart',cart)
        
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        Titem = order['get_cart_items']
        for i in cart:
            try:
                Titem += cart[i]['quantity']
                product=Product.objects.get(id=i)

                total=(product.price)*cart[i]['quantity'] # total=cost
        
                order['get_cart_total']+=total
                order['get_cart_items']+=cart[i]['quantity']
        
                item={
                    'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)
                if product.digital==False:
                    order['shipping']=True
                context = {'items':items, 'order': order,'Titem':Titem}
            except:
                pass
        return {'Titem':Titem,'order':order,'items':items}
def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        orders= Order.objects.filter(customer = customer, complete=False)
        items=[]
        cost=0
        for order in orders:
            for item in order.orderitem.all():
                items.append(item)
        cost = sum(a.get_cart_total for a in orders)
        Titem=sum(a.get_cart_item for a in orders)
        
        shipping=False
        shipping = True if True in [x.shipping for x in orders] else False 
        ''' shipping=True if True in [orders.shipping] else False '''
        context ={'items':items, 'order': order,'Titem':Titem,'shipping':shipping}
        ''' shipping = True if True in [x.shipping for x in orders] else False '''
    else:
        cookieData=cookieCart(request)
        Titem=cookieData['Titem']
        order=cookieData['order']
        items=cookieData['items']
        shipping=False
    return {'Titem':Titem,'order':order,'items':items}
def guestOrder(request,data):
    print('User is not logged in...')
    print('COOKIES:',request.COOKIES)
    name=data['form']['name']
    email=data['form']['email']
    cookieData=cookieCart(request)
    items=cookieData['items']
        
    customer,created=Customer.objects.get_or_create(
        email=email,    
    )
    customer.name=name
    customer.save()
        
    order=Order.objects.create(
        customer=customer,
        complete=False,
        )
    for item in items:
        product=Product.objects.get(id=item['product']['id'])
        orderItem=OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
            )
    
    return customer,order
    
    