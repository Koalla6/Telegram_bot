import matplotlib.pyplot as plt
import os
from aiogram import executor, types
# from telebot import types
from bot import *
from keyboards import *
from messages import *
from translation import translate_phrase
from keyWords import key_words
from channels import channels_rus, channels_ukr, channels_ukr_r
from database import show_russian_channels, show_ukrainian_channels


reply_is_graphics = False

# class Form(StatesGroup):
#     newsText = State()
#     newsGraphic = State()

#keyboards.py
# inline_btn_show_list = InlineKeyboardButton(text = 'Переглянути список каналів', callback_data='choose_list')
# inline_btn_check_news = InlineKeyboardButton(text = 'Перевірити новину', callback_data='choose_type_of_reply')
#
# inline_btn_rus_channels = InlineKeyboardButton(text = 'росіянських', callback_data = 'rus')
# inline_btn_ukr_channels = InlineKeyboardButton(text = 'Українських', callback_data = 'ukr')
# inline_btn_main_menu = InlineKeyboardButton(text = 'Повернутись в головне меню', callback_data = 'main_menu')
#
# inline_btn_graphic = InlineKeyboardButton(text = 'Графічному', callback_data = 'graphic')
# inline_btn_text = InlineKeyboardButton(text = 'Текстовому', callback_data = 'text')
#
# greeting_keyboard = InlineKeyboardMarkup().add(inline_btn_show_list, inline_btn_check_news)
# channels_keyboard = InlineKeyboardMarkup().add(inline_btn_rus_channels, inline_btn_ukr_channels, inline_btn_main_menu)
# reply_keyboard = InlineKeyboardMarkup().add(inline_btn_graphic, inline_btn_text, inline_btn_main_menu)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Переглянути список каналів")
    # btn2 = types.KeyboardButton("Перевірити новину")
    # markup.add(btn1, btn2)
	# bot.reply_to(message, "Привіт")
    # chat_id = message.chat.id

    print("Send Welcome!")
    await message.reply(text = GREETING,
                        reply_markup=greeting_keyboard)
    # bot.send_message(message.chat.id, text = "Привіт, {0.first_name}!\nЯ допоможу тобі дізнатись "
    #                                     "чи є новина, яку ти мені покажеш - фейковою"
    #                                     "\n\nЩо тебе цікавить?".format(message.from_user),
    #                                     reply_markup=greeting_keyboard)

@dp.callback_query_handler(text="choose_list")
async def choose_list(call: types.CallbackQuery):

    print("Choose List!")
    await call.message.answer(text = CHOOSE_LIST, reply_markup=channels_keyboard)

@dp.callback_query_handler(text="choose_type_of_reply")
async def choose_type_of_reply(call: types.CallbackQuery):
    await call.message.answer(text = CHOOSE_TYPE_OF_REPLY, reply_markup=reply_keyboard)

@dp.callback_query_handler(text="main_menu")
async def main_menu(call: types.CallbackQuery):
    print("Main menu")
    await call.message.answer(text = MAIN_MENU, reply_markup=greeting_keyboard)

@dp.callback_query_handler(text="rus")
async def rus_list(call: types.CallbackQuery):
    channels = show_russian_channels()
    for i in channels:
        await call.message.answer(i)
    await call.message.answer(text = CHANNEL_LIST, reply_markup=channels_keyboard)

@dp.callback_query_handler(text="ukr")
async def ukr_list(call: types.CallbackQuery):
    channels = show_ukrainian_channels()
    for i in channels:
        await call.message.answer(i)
    await call.message.answer(text = CHANNEL_LIST, reply_markup=channels_keyboard)

@dp.callback_query_handler(text="graphic")
async def graphic(call: types.CallbackQuery):
    await call.message.answer(text = ASK_FOR_A_NEWS)
    global reply_is_graphics
    reply_is_graphics = True
    while not types.Message:
        await reply(types.Message)

@dp.callback_query_handler(text="text")
async def text(call: types.CallbackQuery):
    await call.message.answer(text = ASK_FOR_A_NEWS)
    global reply_is_graphics
    reply_is_graphics = False
    while not types.Message:
        await reply(types.Message)
    # await call.message.answer(text = CHOOSE_TYPE_OF_REPLY, reply_markup=reply_keyboard)

@dp.message_handler()
async def reply(message: types.Message):
    reply = await get_user_text(message)
    percents_rus = reply[0]
    percents_ukr = reply[1]

    if (reply_is_graphics):
        index = ["росіянські", "Українські"]
        values = [percents_rus, percents_ukr]
        New_Colors = ['red', 'blue']
        plt.bar(index, values, color=New_Colors)
        file_url = set_url(message)
        plt.savefig(file_url, dpi=100)
        plt.show()
        await message.reply_photo(photo=open(file_url, 'rb'))
        os.remove(file_url)

    else:
        if percents_rus >= percents_ukr:
            difference = percents_rus / percents_ukr
            begining = "В росіянських каналах зустрічається в "
        else:
            difference = percents_ukr / percents_rus
            begining = "В українських каналах зустрічається в "

        difference = round(difference + 0.5)
        if difference == 1:
            end = " раз частіше"
        elif difference <= 4:
            end = " рази частіше"
        else:
            end = " разів частіше"
        string = "".join([begining, str(difference), end])

        await message.reply(text=string)


async def get_user_text(message: types.Message):
    print("...")
    text = message.text
    print("text is: ", text)
    await message.reply(text = WAITING)
    # message.reply(text="Обробка інформації...")
    # print(text)
    # bot.reply_to(message, "оце?)")
    translation_src_text = translate_phrase(text)
    translation_src = translation_src_text[0]
    translation_text = translation_src_text[1]
    #bot.reply_to(message, translation_text)
    #word_list = key_words(text)

    if translation_src == "uk":
        print("кацапські слова")
        word_list_ru = key_words(translation_text)
        print("_________________________________________")
        print("українські слова")
        word_list_uk = key_words(text)
        percents_rus = channels_rus(word_list_ru)
        percents_ukr = channels_ukr(word_list_uk)
        percents_ukr_r = channels_ukr_r(word_list_ru)
        percents_ukr += percents_ukr_r
        percents = [percents_rus, percents_ukr]
        return percents
    elif translation_src == "ru":
        word_list_ru = key_words(text)
        word_list_uk = key_words(translation_text)
        percents_rus = channels_rus(word_list_ru)
        percents_ukr = channels_ukr(word_list_uk)
        percents_ukr_r = channels_ukr_r(word_list_ru)
        percents_ukr += percents_ukr_r
        percents = [percents_rus, percents_ukr]
        return percents
    else:
        await message.reply(text = DONT_UNDERSTAND)
        # message.reply(text="Я тебе не розумію :с \nBведи новину росіянською або українською мовою")

def set_url(message: types.Message):
    pic_URL_start = "graphics/"
    pic_name = message.chat.id
    pic_URL_end = ".png"
    pic_URL = "".join([pic_URL_start, str(pic_name), pic_URL_end])
    return pic_URL


# def if_text():
#     reply_text(message)
    # bool = channels_def(word_list)
    # bot.reply_to(message, bool)
    # for w in word_list:
    #     bot.reply_to(message, w)
    #bot.send_message(message.chat.id, message)

# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

# bot.polling(none_stop=True)
# bot.infinity_polling()
executor.start_polling(dp)