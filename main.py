import time
import matplotlib.pyplot as plt
import numpy as np
import asyncio as asyncio
import telebot
from aiogram import Bot, Dispatcher, executor, types
from telebot import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
# import config
from translate import translate_phrase
from keyWords import key_words
from channels import channels_rus, channels_ukr, channels_ukr_r
from database import show_russian_channels, show_ukrainian_channels

bot = Bot(token = "5619682598:AAFC35IX0Ul1zxXF_54dLa-HfADMlTILV4M")
storage = MemoryStorage()
dp = Dispatcher(bot)

class Form(StatesGroup):
    newsText = State()
    newsGraphic = State()

#keyboards.py
inline_btn_show_list = InlineKeyboardButton(text = 'Переглянути список каналів', callback_data='choose_list')
inline_btn_check_news = InlineKeyboardButton(text = 'Перевірити новину', callback_data='choose_type_of_reply')

inline_btn_rus_channels = InlineKeyboardButton(text = 'росіянських', callback_data = 'rus')
inline_btn_ukr_channels = InlineKeyboardButton(text = 'Українських', callback_data = 'ukr')
inline_btn_main_menu = InlineKeyboardButton(text = 'Повернутись в головне меню', callback_data = 'main_menu')

inline_btn_graphic = InlineKeyboardButton(text = 'Графічному', callback_data = 'graphic')
inline_btn_text = InlineKeyboardButton(text = 'Текстовому', callback_data = 'text')

greeting_keyboard = InlineKeyboardMarkup().add(inline_btn_show_list, inline_btn_check_news)
channels_keyboard = InlineKeyboardMarkup().add(inline_btn_rus_channels, inline_btn_ukr_channels, inline_btn_main_menu)
reply_keyboard = InlineKeyboardMarkup().add(inline_btn_graphic, inline_btn_text, inline_btn_main_menu)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # btn1 = types.KeyboardButton("Переглянути список каналів")
    # btn2 = types.KeyboardButton("Перевірити новину")
    # markup.add(btn1, btn2)
	# bot.reply_to(message, "Привіт")
    # chat_id = message.chat.id
    await message.reply(text = "Привіт!\nЯ допоможу тобі дізнатись "
                            "чи є новина, яку ти мені покажеш - фейковою"
                            "\n\nЩо тебе цікавить?",
                        reply_markup=greeting_keyboard)
    # bot.send_message(message.chat.id, text = "Привіт, {0.first_name}!\nЯ допоможу тобі дізнатись "
    #                                     "чи є новина, яку ти мені покажеш - фейковою"
    #                                     "\n\nЩо тебе цікавить?".format(message.from_user),
    #                                     reply_markup=greeting_keyboard)

@dp.callback_query_handler(text="choose_list")
async def choose_list(call: types.CallbackQuery):
    await call.message.answer(text = "Який список каналів ти хочеш переглянути?", reply_markup=channels_keyboard)

@dp.callback_query_handler(text="choose_type_of_reply")
async def choose_type_of_reply(call: types.CallbackQuery):
    await call.message.answer(text = "В якиму вигляді бажаєш отримати відповідь?", reply_markup=reply_keyboard)

@dp.callback_query_handler(text="main_menu")
async def main_menu(call: types.CallbackQuery):
    await call.message.answer(text="\n\nЩо тебе цікавить?", reply_markup=greeting_keyboard)

@dp.callback_query_handler(text="rus")
async def rus_list(call: types.CallbackQuery):
    channels = show_russian_channels()
    for i in channels:
        await call.message.answer(i)
    await call.message.answer(text = "Який список каналів ти хочеш переглянути?", reply_markup=channels_keyboard)
    # await call.russian_channels

@dp.callback_query_handler(text="ukr")
async def ukr_list(call: types.CallbackQuery):
    channels = show_ukrainian_channels()
    for i in channels:
        await call.message.answer(i)
    await call.message.answer(text="Який список каналів ти хочеш переглянути?", reply_markup=channels_keyboard)

@dp.callback_query_handler(text="graphic")
async def graphic(call: types.CallbackQuery):
    await call.message.answer(text="Встав текст новини у поле поле вводу")
    while not types.Message:
        await reply_graphics(types.Message)

@dp.callback_query_handler(text="text")#, content_types=types.ContentTypes.TEXT)
async def text(call: types.CallbackQuery): #message: types.Message,
    # news = yield from reply_text("Встав текст новини у поле поле вводу")
    # if news:
    #     reply_text(news)
    # await Form.newsText.set()
    await call.message.answer(text="Встав текст новини у поле поле вводу")
    # await asyncio.gather(reply_text)
    while not types.Message:
        await reply_text(types.Message)

    # register_next_step_handler(self, message: types.Message, callback: Callable, *args, **kwargs) -> None:
    #await reply_text(message)
    # time.sleep(5000)

    # reply_text(message=chat.id)

@dp.message_handler()
async def reply_graphics(message: types.Message):
    reply = await get_user_text(message)
    percents_rus = reply[0]
    percents_ukr = reply[1]
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1])
    index = ["росіянські", "Українські"]
    values = [percents_rus, percents_ukr]
    New_Colors = ['red', 'blue']
    # fig = plt.subplots()
    plt.bar(index, values, color=New_Colors)
    # plt.legend()
    plt.show()
    plt.savefig("graphics/graphic.png")
    # plt.savefig('D:/політех/6 курс/диплом/pythonProject/TB/graphics/графік.png')
    # await message.reply(plt.show())

@dp.message_handler()
async def reply_text(message: types.Message):
    # print("HERE")#, state: FSMContext):
    reply = await get_user_text(message)
    percents_rus = reply[0]
    percents_ukr = reply[1]
    if percents_rus >= percents_ukr:
        difference = percents_rus / percents_ukr
        begining = "В росіянських каналах зустрічається в "
    else:
        difference = percents_ukr / percents_rus
        begining = "В українських каналах зустрічається в "

    difference = round(difference+0.5)
    if difference == 1:
        end = " раз частіше"
    elif difference <= 4:
        end = " рази частіше"
    else:
        end = " разів частіше"
    string = "".join([begining, str(difference), end])

    await message.reply(text=string)

# @dp.message_handler(content_types=types.ContentTypes.TEXT)
# async def

# @dp.message_handler(state=Form.newsText)
# async def reply_text(message: types.Message, state: FSMContext):
#     print("HERE")#, state: FSMContext):
#     async with state.proxy() as data:
#         data['newsText'] = message.text
#         reply = get_user_text(data['newsText'])
#         persents_rus = reply[0]
#         persents_ukr = reply[1]
#         ros = "Зустрічається в росіянців - "
#         ukr = "\nЗустрічається в українських тг каналах - "
#         string = "".join([ros, str(persents_rus), ukr, str(persents_ukr)])
#         await message.reply(message, string)


# @bot.message_handler()
# def func(message):
    # if (message.text == "Переглянути список каналів"):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("росіянських")
    #     btn2 = types.KeyboardButton("Українських")
    #     back = types.KeyboardButton("Повернутись в головне меню")
    #     markup.add(btn1, btn2, back)
    #     bot.send_message(message.chat.id, text="Який список каналів ти хочеш переглянути?", reply_markup=markup)
    # elif (message.text == "Перевірити новину"):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Графічному")
    #     btn2 = types.KeyboardButton("Текстовому")
    #     back = types.KeyboardButton("Повернутись в головне меню")
    #     markup.add(btn1, btn2, back)
    #     bot.send_message(message.chat.id, text="В якиму вигляді бажаєш отримати відповідь?", reply_markup=markup)
    # elif (message.text == "Повернутись в головне меню"):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btn1 = types.KeyboardButton("Переглянути список каналів")
    #     btn2 = types.KeyboardButton("Перевірити новину")
    #     markup.add(btn1, btn2)
    #     bot.send_message(message.chat.id, text="Головне меню",
    #                      reply_markup=markup)
    # elif (message.text == "росіянських"):
    #     channels = show_russian_channels()
    #     for i in channels:
    #         bot.send_message(message.chat.id, i)
    #     # bot.send_message(message.chat.id, channels)
    #     # bot.send_message(message.chat.id, '\n'.join(channels))
    # elif (message.text == "Українських"):
    #     channels = show_ukrainian_channels()
    #     for i in channels:
    #         bot.send_message(message.chat.id, i)
    # elif (message.text == "Графічному"):
    #     bot.send_message(message.chat.id, text="Встав текст новини у поле поле вводу")
    #     # get_user_text(message)
    # elif (message.text == "Текстовому"):
    #     bot.send_message(message.chat.id, text="Встав текст новини у поле поле вводу")
    #     reply_text(message)
    # else:
    #     # get_user_text(message)
# @dp.callback_query_handler()
# async def russian_channels(call: types.CallbackQuery):
#     channels = show_russian_channels()
#     for i in channels:
#         await call.message.answer(i)
        # bot.send_message(i)


@dp.message_handler()
async def get_user_text(message: types.Message):
    print("...")
    text = message.text
    await message.reply(text = "Обробка інформації...")
    # print(text)
    # bot.reply_to(message, "оце?)")
    translation_src_text = translate_phrase(text)
    translation_src = translation_src_text[0]
    translation_text = translation_src_text[1]
    #bot.reply_to(message, translation_text)
    #word_list = key_words(text)

    if translation_src == "uk":
        word_list_ru = key_words(translation_text)
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
        await message.reply(text = "Я тебе не розумію :с \nBведи новину росіянською або українською мовою")



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