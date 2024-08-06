import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(class_payment):
    if class_payment.lesson is None:
        product = stripe.Product.create(name=class_payment.course)
        return product.get("id")
    elif class_payment.course is None:
        product = stripe.Product.create(name=class_payment.lesson)
        return product.get("id")
    else:
        raise ValueError("Введите курс или урок для покупки")


def create_stripe_prise(amount):
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        cancel_url="http://localhost:8000/",
        line_items=[{"price": price["id"], "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
