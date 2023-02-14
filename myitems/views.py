from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
import stripe
from .models import Item, Order
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_API_SECRET_KEY
stripe_usd_api_key = settings.STRIPE_API_USD_SECRET_KEY
stripe_eur_api_key = settings.STRIPE_API_EUR_SECRET_KEY

@api_view(['GET'])
def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item': item,
        'session_id': '',
        'stripe_api_key': stripe.api_key,
    }
    return render(request, 'item_detail.html', context)

@api_view(['GET'])
def buy_order(request, order_id):
    order = Order.objects.get(id=order_id)
    items = order.items.all()
    order_total = sum([item.price for item in items])
    
    if order.discount:
        order_total -= order.discount.amount
    
    if order.tax:
        order_total += order.tax.amount
    
    stripe.api_key = stripe_usd_api_key if order.currency == "usd" else stripe_eur_api_key

    # Create a Payment Intent
    payment_intent = stripe.PaymentIntent.create(
        amount=order_total,
        currency=order.currency,
        description=f"Payment for Order {order.id}"
    )
    
    return redirect(f'https://checkout.stripe.com/pay/{payment_intent.id}')

@api_view(['GET'])
def buy_item(request, item_id):
    item = Item.objects.get(id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'quantity': 1,
                'price_data':{
                    'unit_amount': int(item.price * 100),
                    'currency': 'usd',
                    'product_data':{
                        'name': item.name,
                        'description': item.description,
                    }
                }
            }
        ],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return JsonResponse({"session_id": session.id})

@api_view(['GET'])
def buy_item_redirect(request, item_id):
    item = Item.objects.get(id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'quantity': 1,
                'price_data':{
                    'unit_amount': int(item.price * 100),
                    'currency': 'usd',
                    'product_data':{
                        'name': item.name,
                        'description': item.description,
                    }
                }
            }
        ],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return redirect(f'https://checkout.stripe.com/session/{session.id}')

def buy_item_intent(request, item_id):
    item = Item.objects.get(id=item_id)
    
    stripe.api_key = stripe_usd_api_key if item.currency == "usd" else stripe_eur_api_key

    # Create a Payment Intent
    payment_intent = stripe.PaymentIntent.create(
        amount=item.price,
        currency=item.currency,
        description=f"Payment for Item {item.id}"
    )

    return JsonResponse({"payment_intent_id": payment_intent.id})