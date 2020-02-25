from telegram import ReplyKeyboardMarkup, KeyboardButton

from bot import constants
from product.models import Category, Product


def back_markup(lang):
    return ReplyKeyboardMarkup([
        [constants.messages[lang][constants.back_menu]]
    ])


def finish_order_markup(lang):
    return ReplyKeyboardMarkup([
        [constants.messages[lang][constants.finish_order_menu]],
        [constants.messages[lang][constants.back_menu]]
    ])


register_markup = ReplyKeyboardMarkup([
    [KeyboardButton(text=constants.send_contact_menu, request_contact=True)]
])


def home_markup(lang):
    home = [
        [constants.messages[lang][constants.make_order_menu]],
        [constants.messages[lang][constants.cart_menu],
         constants.messages[lang][constants.my_orders_menu]],
        [constants.messages[lang][constants.language_menu],
         constants.messages[lang][constants.feedback_menu]]
    ]
    return ReplyKeyboardMarkup(home)


languages = [
    ["🇺🇿 O'zbekcha"], ['🇷🇺 Русский', '🇺🇸 English']
]
languages_markup = ReplyKeyboardMarkup(languages)


def categories_markup(lang):
    if lang == 'en':
        categories = list(Category.objects.filter(
            available=True).values_list('name_en', flat=True))
    elif lang == 'ru':
        categories = list(Category.objects.filter(
            available=True).values_list('name_ru', flat=True))
    else:
        categories = list(Category.objects.filter(
            available=True).values_list('name', flat=True))
    categories.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([categories[i:i + 2] for i in range(0, len(categories), 2)])


def product_list(category_id, lang):
    if lang == 'en':
        products = list(Product.objects.filter(
            category_id=category_id).values_list('name_en', flat=True))
    elif lang == 'ru':
        products = list(Product.objects.filter(
            category_id=category_id).values_list('name_ru', flat=True))
    else:
        products = list(Product.objects.filter(
            category_id=category_id).values_list('name', flat=True))
    products.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup([products[i:i + 2] for i in range(0, len(products), 2)])


pieces = [str(x) for x in (range(1, 10))]


def pieces_markup(lang):
    pieces.append(constants.messages[lang][constants.back_menu])
    return ReplyKeyboardMarkup(
        [pieces[i:i + 3] for i in range(0, len(pieces), 3)])
