from django.conf import settings
from .models import CreditCard, Transaction
import requests, json, uuid

def prepare_checkout_data(request, product=None):
    cards = []
    # :user/:product/:transaction
    transaction_id = str(uuid.uuid4())

    data = {
        "authentication.userId": settings.PEACH_USER_ID,
        "authentication.password": settings.PEACH_PASSWORD,
        "authentication.entityId": settings.PEACH_ENTITY_RECURRING_ID,
        "createRegistration": True,
        "paymentType": "DB"
    }

    if product is not None:
        transaction_id = '{}/{}'.format(request.user.id, transaction_id)
        price = int(product.price)
        data['currency'] = product.currency
        data['amount'] = price

        data['cart.items[0].name'] = product.title
        data['cart.items[0].merchantItemId'] = product.id
        data['cart.items[0].quantity'] = 1
        data['cart.items[0].price'] = price
        data['cart.items[0].originalPrice'] = price

    if request.user and request.user.is_authenticated():
        cards = CreditCard.objects.filter(user=request.user)
        transaction_id = '{}/{}'.format(request.user.id, transaction_id)

    data['merchantTransactionId'] = transaction_id

    for index, card in enumerate(cards):
        key = 'registrations[{}].id'.format(index)
        data[key] = card.registration_id


    return data

def save_card(user, registration_id, data):
    card = {
        'user_id': user.id,
        'registration_id': registration_id,
        'cardholder_name': data.get('holder'),
        'expiry_month': data.get('expiryMonth'),
        'expiry_year': data.get('expiryYear'),
        'last_four_digits': data.get('last4Digits'),
        'bin': data.get('bin'),
    }
    return CreditCard.objects.create(**card)

def save_transaction(user, data):

    transaction = {
        # "user_id": user.id,
        "currency": data.get('currency'),
        "price": data.get('amount'),
        "transaction_id": data.get('id'),
        "ndc": data.get('ndc'),
        "payment_brand": data.get('paymentBrand'),
        "payment_type": data.get('paymentType'),
        "registration_id": data.get('registrationId'),
        "result_code": data.get('result', {}).get('code'),
        "result_description": data.get('result', {}).get('description'),
        "data": json.dumps(data)
    }

    transaction = Transaction.objects.create(**transaction)
    if data.get('card', None) is not None:
        card = save_card(user, data.get('registrationId'), data.get('card'))
        transaction.card = card
        transaction.save()

    return transaction

def repeat_payment():
    '''
    curl https://test.oppwa.com/v1/registrations/../payments \
    -d "authentication.userId=.." \
    -d "authentication.password=.." \
    -d "authentication.entityId=.." \
    -d "amount=92.00" \
    -d "currency=ZAR" \
    -d "paymentType=DB" \
    -d "recurringType=REPEATED"
    '''
    pass