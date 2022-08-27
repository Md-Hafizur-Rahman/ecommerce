from django import template
from store.models import Order



register = template.Library()

@register.simple_tag(takes_context=True)
def total_item(context):
    request = context.get("request")
    usr = request.user.customer
    if usr and Order.objects.filter(customer=usr, complete=False).exists():
        order = Order.objects.filter(customer=usr, complete=False).first()
        return order.get_cart_item
    else:
        return 0