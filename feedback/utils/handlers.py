import telebot
import json
from .i18n import CONTENT
from .exception import MessageException
from user.models import TelegramUser
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton

bot = telebot.TeleBot("BOTID")

@csrf_exempt
def webhook(request):
    # https://9609-213-230-102-106.eu.ngrok.io/feedback/send/bot
    if request.method == 'POST':
        data = Payload(request=request).get_webhook_data()
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return HttpResponse('OK', {"success": True})


class MessageInterface:
    data = None

    def __init__(self, request):
        try:
            data = request.body.decode("utf-8")
            self.data = json.loads(data)
            if self.data is None:
                MessageException(message='ERROR INVALID JSON OBJECT', code=MessageException.ERROR_INVALID_JSON_OBJECT)
        except TypeError or ValueError:
            MessageException(message='ERROR CAN NOT PARSING JSON', code=MessageException.ERROR_CAN_NOT_PARSING_JSON)


class Payload(MessageInterface):
    """ Processing the payload object."""

    def __init__(self, request):
        super().__init__(request)
        self.payload = self.data

    # Get the type of a user_id
    def get_type(self):
        return self.payload["user"]

    # Get messages from payload
    def get_webhook_data(self):
        return self.payload

    # Get messages from payload
    def get_messages(self):
        data = self.payload
        if isinstance(data["message"], list):
            message = " ".join(data["message"])
        else:
            message = data["message"]
        return message


class MessageHandler:
    def __init__(self, chat_id=None, username=None, phone=None, text=None, secret_key=None, message_id=None):
        self.chat_id = chat_id
        self.username = username
        self.phone = phone
        self.text = text
        self.secret_key = secret_key
        self.message_id = message_id

    def select_language(self):
        buttons = ReplyKeyboardMarkup(True, False, row_width=3)
        lang_uz = InlineKeyboardButton(text='UZ🇺🇿', callback_data='lang_uz')
        lang_en = InlineKeyboardButton(text='EN🇺🇸', callback_data='lang_en')
        lang_ru = InlineKeyboardButton(text='RU🇷🇺', callback_data='lang_ru')
        buttons.add(lang_uz, lang_en, lang_ru)
        bot.send_message(self.chat_id, "<b>Tilni tanlang!</b>", reply_markup=buttons, parse_mode='HTML')

    def start(self):
        self.signup()
        print(self.chat_id)
        bot.send_message(self.chat_id, "Assalomu aleykum")
        self.select_language()

    def signup(self):
        qs = TelegramUser.objects.filter(chat_id=self.chat_id)
        if qs.exists():
            qs.update(chat_id=self.chat_id, username=self.username, phone=self.phone, step=1)
        else:
            TelegramUser.objects.create(chat_id=self.chat_id, username=self.username, phone=self.phone, step=1)

    def create_account_uz(self):
        print(self.chat_id)
        qs = TelegramUser.objects.filter(chat_id=self.chat_id)
        qs.update(chat_id=self.chat_id, phone=self.phone, step=2, lang="UZ")
        bot.send_message(self.chat_id, "E-mail manzilingizni kiriting!", reply_markup=ReplyKeyboardRemove())

    def create_account_en(self):
        print(self.chat_id)
        qs = TelegramUser.objects.filter(chat_id=self.chat_id)
        qs.update(chat_id=self.chat_id, phone=self.phone, step=2, lang="EN")
        bot.send_message(self.chat_id, "Enter your email address!", reply_markup=ReplyKeyboardRemove())

    def create_account_ru(self):
        print(self.chat_id)
        qs = TelegramUser.objects.filter(chat_id=self.chat_id)
        qs.update(chat_id=self.chat_id, phone=self.phone, step=2, lang="RU")
        bot.send_message(self.chat_id, "Введите ваш адрес электронной почты!", reply_markup=ReplyKeyboardRemove())

    def enter_valid_email(self):
        user = TelegramUser.objects.get(chat_id=self.chat_id)
        message = CONTENT.get(user.lang, "UZ")
        bot.send_message(self.chat_id, f"<b>{message}</b>", parse_mode='HTML')

    def main(self):
        user = TelegramUser.objects.get(chat_id=self.chat_id)
        if user.step == 0:
            bot.send_message(self.chat_id, "<b>Tilni tanlang!</b>", parse_mode='HTML')
            self.select_language()
        elif user.step == 1:
            if self.text[:2] == "UZ":
                self.create_account_uz()
            elif self.text[:2] == "EN":
                self.create_account_en()
            elif self.text[:2] == "RU":
                self.create_account_ru()
            else:
                self.select_language()
        elif user.step == 2:
            self.enter_valid_email()
        else:
            self.start()


@bot.message_handler(commands=['start'])
def start(message):
    MessageHandler(chat_id=message.chat.id, username=message.from_user.username).start()


@bot.message_handler(content_types='text')
def send_message(message):
    # print("send_message > ", message)
    MessageHandler(chat_id=message.chat.id, text=message.text, message_id=message.message_id).main()


# Inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'lang_ru':
        print('press button "text"')
    elif call.data == 'menu':
        print('"press button menu"')
