# for user language choices
UZ = 'uz'
EN = 'en'
RU = 'ru'
LANGUAGES = [
    (UZ, "O'zbekcha"),
    (EN, 'English'),
    (RU, 'Русский')
]

# for last command writing
register = 'register'
home = 'home'
category = 'category'
product = 'product'
language = 'language'
feedback = 'feedback'
pieces = 'pieces'
cart = 'cart'
add_to_cart = 'add to cart'
finish_order = 'finish_order'
back = 'back'

# for menus
make_order_menu = '🛒 Make order'
cart_menu = '🛒 Cart'
my_orders_menu = '🛍 My Orders'
language_menu = '🇺🇿 🇷🇺 🇺🇸 Language'
feedback_menu = '✍️ Feedback'
back_menu = 'Back'
finish_order_menu = 'Finish order'
send_contact_menu = "Send contact"

# for messages
register_succeed_msg = "Thank you for registration!"
ask_contact_msg = "Click 'send contact' to register."
welcome_msg = 'Welcome'
empty_cart_msg = "Your cart is empty"
lang_select_msg = "Language has changed"
feedback_succeed_msg = 'Thanks for your feedback!'
feedback_send_msg = 'Enter text below and send.'
in_your_cart = "In your cart:"
no_orders_yet_msg = "You didn't order anything yet."
your_orders_msg = "Your orders:"
status_msg = 'Status'
ordered_msg = 'Ordered'
delivered_msg = 'Delivered'
choose_type_msg = 'Choose type'
added_to_card_msg = '{} pieces {} added to cart'
finished_message = 'Finished'
messages = {
    'uz': {
        welcome_msg: 'Xush kelibsiz!',
        empty_cart_msg: "Savatchangiz bo'sh",
        lang_select_msg: "Til o'zgardi",
        feedback_succeed_msg: "Fikr va mulohazalaringiz uchun rahmat!",
        feedback_send_msg: "Quyida matn kiriting va junating",
        in_your_cart: "Savatchada:",
        your_orders_msg: "Buyurtmalaringiz:",
        status_msg: 'Holati',
        ordered_msg: 'Buyurtma vaqti',
        delivered_msg: 'Yetkazish vaqti',
        choose_type_msg: 'Turini tanlang:',
        added_to_card_msg: '{} dona {} savatchaga qo\'shildi',
        no_orders_yet_msg: "Siz hanuz buyurtma qilmagansiz.",
        make_order_menu: '🛒 Buyurtma berish',
        cart_menu: '🛒 Savatcha',
        my_orders_menu: '🛍 Mening buyurtmalarim',
        language_menu: '🇺🇿 🇷🇺 🇺🇸 Til',
        feedback_menu: '✍️ Taklif bildirish',
        back_menu: 'Orqaga',
        finish_order_menu: 'Buyurtmani yakunlash',
        finished_message: 'Amalga oshirildi!',
    },
    'en': {
        welcome_msg: 'Welcome!',
        empty_cart_msg: "Your cart is empty",
        lang_select_msg: "Language has changed",
        feedback_succeed_msg: 'Thanks for your feedback!',
        feedback_send_msg: 'Enter text below and send.',
        in_your_cart: "In your cart:",
        your_orders_msg: "Your orders:",
        status_msg: 'Status',
        ordered_msg: 'Ordered',
        delivered_msg: 'Delivered',
        choose_type_msg: 'Choose type:',
        added_to_card_msg: '{} pieces {} added to cart',
        no_orders_yet_msg: "You didn't order anything yet.",
        make_order_menu: '🛒 Make order',
        cart_menu: '🛒 Cart',
        my_orders_menu: '🛍 My Orders',
        language_menu: '🇺🇿 🇷🇺 🇺🇸 Language',
        feedback_menu: '✍️ Feedback',
        back_menu: 'Back',
        finish_order_menu: 'Finish order',
        finished_message: 'Success!',
    },
    'ru': {
        welcome_msg: 'Добро пожаловать!',
        empty_cart_msg: "Ваша корзина пуста",
        lang_select_msg: "Язык изменен",
        feedback_succeed_msg: 'Спасибо за ваш отзыв!',
        feedback_send_msg: "Введите текст ниже и отправьте.",
        in_your_cart: "В корзине:",
        your_orders_msg: "Ваши заказы:",
        status_msg: 'Состояние',
        ordered_msg: 'Заказано',
        delivered_msg: 'Доставлен',
        choose_type_msg: 'Выберите тип:',
        added_to_card_msg: '{} шт. {} добавлен в корзину',
        no_orders_yet_msg: "Вы еще ничего не заказывали.",
        make_order_menu: '🛒 Сделать заказ',
        cart_menu: '🛒 Корзина',
        my_orders_menu: '🛍 Мои заказы',
        language_menu: '🇺🇿 🇷🇺 🇺🇸 Язык',
        feedback_menu: '✍️ Обратная связь',
        back_menu: 'Назад',
        finish_order_menu: 'Завершить заказ',
        finished_message: 'Успешно!',
    },

}
