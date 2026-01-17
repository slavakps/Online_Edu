import stripe
from django.conf import settings

# Настраиваем Stripe с нашим секретным ключом
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name, description):
    """Создает продукт в Stripe"""
    try:
        print(f"Пытаемся создать продукт: {name}")

        if not description:
            description = f"Курс: {name}"

        product = stripe.Product.create(
            name=name,
            description=description
        )
        print(f"Продукт создан: {product.id}")
        return product
    except Exception as e:
        print(f"Ошибка создания продукта: {e}")
        return None


def create_price(product_id, amount, currency='usd'):
    """Создает цену для продукта в Stripe"""
    try:
        print(f"Пытаемся создать цену для продукта {product_id}: {amount}")
        # amount в копейках (умножаем на 100)
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),  # переводим в копейки
            currency=currency
        )
        print(f"Цена создана: {price.id}")
        return price
    except Exception as e:
        print(f"Ошибка создания цены: {e}")
        return None


def create_checkout_session(price_id, success_url, cancel_url):
    """Создает сессию оплаты в Stripe и возвращает URL для оплаты"""
    try:
        print(f"Пытаемся создать сессию для цены {price_id}")
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        print(f"Сессия создана: {session.url}")
        return session
    except Exception as e:
        print(f"Ошибка создания сессии: {e}")
        return None