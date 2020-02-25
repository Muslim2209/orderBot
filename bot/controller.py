from django.db.models import Sum, F, Q

from bot import markups, constants
from bot.models import Command, Feedback
from product.models import Order, Product, CartItem, Category


def command_logging(user, message_id, text, from_menu=None, current_menu=None, to_menu=None):
    Command.objects.create(user=user,
                           message_id=message_id,
                           text=text,
                           from_menu=from_menu,
                           current_menu=current_menu,
                           to_menu=to_menu)


class Controller:
    def __init__(self, bot, update, user, cart=None, last_command=None):
        self.bot = bot
        self.update = update
        self.user = user
        self.cart = cart
        self.last_command = last_command

    def get_lang(self):
        if self.user.language == markups.languages[1][1]:
            return 'en'
        elif self.user.language == markups.languages[1][0]:
            return 'ru'
        else:
            return 'uz'

    def start(self):
        text = 'Welcome {}!\n'.format(
            self.user.first_name if self.user.first_name else 'User')
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def home_control(self):
        if self.update.message.text == constants.messages[self.get_lang()][constants.make_order_menu]:
            self.category_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.cart_menu]:
            self.cart_check()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.my_orders_menu]:
            self.order_history()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.language_menu]:
            self.language_select()

        elif self.update.message.text == constants.messages[self.get_lang()][constants.feedback_menu]:
            self.feedback()

        # else:
        #     self.bot.sendMessage(self.update.message.chat_id, text='? in ?')

    def cart_check(self):
        cart_items = self.cart.all()
        if not cart_items.exists():
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=constants.messages[self.get_lang()][constants.empty_cart_msg],
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.home,
                            to_menu=constants.home)

        else:
            pcs = cart_items.values_list('quantity', flat=True)
            prods = cart_items.values_list('product__name', flat=True)
            zipped = zip(pcs, prods)

            items_str = ''
            for i, j in zipped:
                items_str += (str(i) + ' x ' + j + '\n')

            total = self.cart.aggregate(Total=Sum(F('price')))

            text = '{}\n{}\nTotal: {}'.format(constants.messages[self.get_lang()][constants.in_your_cart],
                                              items_str,
                                              total['Total'])

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.finish_order_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.finish_order,
                            to_menu=constants.home)

    def order_history(self):
        orders_history = Order.objects.filter(user=self.user)
        if orders_history.count() == 0:
            text = constants.messages[self.get_lang()][constants.no_orders_yet_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)
        else:
            statuses = orders_history.values_list('status', flat=True)
            created_at = orders_history.values_list('created', flat=True)
            updated_at = orders_history.values_list('updated', flat=True)
            zipped = zip(statuses, created_at, updated_at)
            order_str = '{}:\n№.| {} \t | \t {} \t | \t {}\n'.format(
                constants.messages[self.get_lang()][constants.your_orders_msg],
                constants.messages[self.get_lang()][constants.status_msg],
                constants.messages[self.get_lang()][constants.ordered_msg],
                constants.messages[self.get_lang()][constants.delivered_msg],
            )
            counter = 1
            for i, j, k in zipped:
                order_str += '{}.| {} | {} | {}\n'.format(counter, i, j, k)
                counter += 1

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=order_str)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

    def language_select(self):
        if self.last_command.to_menu == constants.language and \
                any(self.update.message.text in x for x in markups.languages):
            self.user.language = self.update.message.text
            self.user.save()

            text = constants.messages[self.get_lang()][constants.lang_select_msg]

            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            self.bot.sendMessage(self.update.message.chat_id,
                                 text='Choose your language:',
                                 reply_markup=markups.languages_markup)
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.language)

    def feedback(self):
        if self.last_command.current_menu == constants.feedback:
            Feedback.objects.create(user=self.user,
                                    text=self.update.message.text)
            text = constants.messages[self.get_lang()][constants.feedback_succeed_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.home_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            to_menu=constants.home)

        elif self.last_command.from_menu == constants.home:
            text = constants.messages[self.get_lang()][constants.feedback_send_msg]
            self.bot.sendMessage(self.update.message.chat_id,
                                 text=text,
                                 reply_markup=markups.back_markup(self.get_lang()))
            command_logging(user=self.user,
                            message_id=self.update.message.message_id,
                            text=self.update.message.text,
                            from_menu=constants.home,
                            current_menu=constants.feedback,
                            to_menu=constants.home)

    def go_home(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.welcome_msg],
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def go_back(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text='Back',
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        to_menu=constants.home)

    def add_to_card(self):
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.add_to_cart,
                        to_menu=constants.product)

        try:
            product = Product.objects.get(
                Q(name=self.last_command.text) |
                Q(name_en=self.last_command.text) |
                Q(name_ru=self.last_command.text)
            )
        except Product.DoesNotExist:
            product = None
            return self.bot.sendMessage(self.update.message.chat_id,
                                        text='Enter valid product',
                                        reply_markup=markups.categories_markup(self.get_lang()))

        quantity = int(self.update.message.text)

        if product and 0 < quantity < 9:
            if (product.id,) in self.cart.values_list('product_id'):
                item = self.cart.get(product_id=product.id)
                item.quantity += quantity
                item.save()
            else:
                CartItem.objects.create(user=self.user, product=product, quantity=quantity)
        else:
            return self.bot.sendMessage(self.update.message.chat_id,
                                        text='Incorrect quantity {}'.format(
                                            self.update.message.text),
                                        reply_markup=markups.categories_markup(self.get_lang()))
        text = constants.messages[self.get_lang()][constants.added_to_card_msg].format(
            self.update.message.text,
            self.last_command.text,
        )
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             reply_markup=markups.categories_markup(self.get_lang()))

    def category_select(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text='Menu',
                             reply_markup=markups.categories_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.home,
                        current_menu=constants.category,
                        to_menu=constants.product)

    def product_select(self):
        category = Category.objects.get(
            Q(name=self.update.message.text) |
            Q(name_en=self.update.message.text) |
            Q(name_ru=self.update.message.text)
        )
        markup = markups.product_list(category.id, self.get_lang())
        text = constants.messages[self.get_lang()][constants.choose_type_msg]
        self.bot.sendMessage(self.update.message.chat_id,
                             text=text,
                             reply_markup=markup)
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.category,
                        current_menu=constants.product,
                        to_menu=constants.pieces)

    def pieces_select(self):
        self.bot.sendMessage(self.update.message.chat_id,
                             text=self.update.message.text,
                             reply_markup=markups.pieces_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.product,
                        current_menu=constants.pieces,
                        to_menu=constants.add_to_cart)

    def finish_order(self):
        order = Order(user=self.user)
        order.save()
        order.cart.set(self.cart)
        self.cart.delete()
        self.bot.sendMessage(self.update.message.chat_id,
                             text=constants.messages[self.get_lang()][constants.finished_message],
                             reply_markup=markups.home_markup(self.get_lang()))
        command_logging(user=self.user,
                        message_id=self.update.message.message_id,
                        text=self.update.message.text,
                        from_menu=constants.finish_order,
                        to_menu=constants.home)
