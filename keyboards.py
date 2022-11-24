from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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