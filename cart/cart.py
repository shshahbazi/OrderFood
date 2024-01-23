from decimal import Decimal
from django.conf import settings
from food.models import Food


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, food):
        food_id = str(food.id)
        if food_id not in self.cart:
            self.cart[food_id] = {'quantity': 1, 'price': str(food.price)}
        else:
            self.cart[food_id]['quantity'] += 1
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, food):
        food_id = str(food.id)
        if food_id in self.cart:
            if self.cart[food_id]['quantity'] > 1:
                self.cart[food_id]['quantity'] -= 1
            else:
                del self.cart[food_id]

            self.save()

    def __iter__(self):
        food_ids = self.cart.keys()
        foods = Food.objects.filter(id__in=food_ids)
        for food in foods:
            self.cart[str(food.id)]['food'] = food

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
