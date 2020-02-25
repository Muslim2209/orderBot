from bot.models import TelegramUser
from product.models import Product, Cart, CartItem, Order

user = TelegramUser.objects.last()
cart = Cart.objects.create(user=user)
product = Product.objects.last()
cart_item = CartItem.objects.create(cart=cart, product=product)
order = Order.objects.create(cart=cart)
