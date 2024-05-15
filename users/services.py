import stripe
from rest_framework import status

from config.settings import STRIPE_API_KEY, CURRENCY_API_URL, CURRENCY_API_KEY
import requests

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(payment):
    """Создание продукта в Stripe"""

    stripe_product = stripe.Product.create(name=payment)
    return stripe_product['id']


def create_stripe_price(amount, product_id):
    """Создание цены в stripe"""
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=amount * 100,
        product=product_id,
    )
    return stripe_price['id']


def create_stripe_session(price):
    """Создание сессии на оплату в Stripe"""
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price, "quantity": 1}],
        mode="payment",
    )
    return stripe_session.get('id'), stripe_session.get('url')
