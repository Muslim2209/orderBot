from django_telegrambot.apps import DjangoTelegramBot
from telegram.ext import MessageHandler, Filters

from bot import constants
from bot.base_commands import register, sticker
from bot.controller import Controller
from bot.models import TelegramUser, Command


def bot_control(bot, update):
    user, created = TelegramUser.objects.get_or_create(
        telegram_id=update.message.chat_id)
    if created:
        user.first_name = update.message.from_user.first_name
        user.last_name = update.message.from_user.last_name
        user.username = update.message.from_user.username
        user.save()

    try:
        cart = user.cart.all()
    except:
        cart = None
    if not user.is_registered:
        return register(bot, user, update)

    if update.message.text == '/start':
        Controller(bot, update, user).start()

    try:
        last_command = Command.objects.filter(user=user).last()
    except Command.DoesNotExist:
        last_command = None

    if update.message.text == 'Home':
        Controller(bot, update, user).go_home()

    elif update.message.text in ["Orqaga", 'Back', "Назад", "orqaga", 'back', "назад"]:
        Controller(bot, update, user).go_home()

    elif last_command.to_menu == constants.language:
        Controller(bot, update, user, cart, last_command).language_select()

    elif last_command.to_menu == constants.category:
        Controller(bot, update, user, cart, last_command).category_select()

    elif last_command.to_menu == constants.product:
        Controller(bot, update, user, cart, last_command).product_select()

    elif last_command.to_menu == constants.pieces:
        Controller(bot, update, user, cart, last_command).pieces_select()

    elif last_command.to_menu == constants.add_to_cart:
        Controller(bot, update, user, cart, last_command).add_to_card()

    elif last_command.current_menu == constants.finish_order:
        Controller(bot, update, user, cart, last_command).finish_order()

    elif last_command.current_menu == constants.feedback:
        Controller(bot, update, user, cart, last_command).feedback()

    elif last_command.to_menu == constants.home:
        Controller(bot, update, user, cart, last_command).home_control()

    else:
        bot.sendMessage(update.message.chat_id, text='???')


def main():
    dp = DjangoTelegramBot.dispatcher

    dp.add_handler(MessageHandler(Filters.all, bot_control))

    dp.add_handler(MessageHandler(Filters.sticker, sticker))
