from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


#здесь расположены все кнопки


main = InlineKeyboardMarkup(inline_keyboard=[
    #[InlineKeyboardButton(text = 'создать модуль', callback_data='add_module')],
    [InlineKeyboardButton(text= 'Создать карту', callback_data='add_card')],
    [InlineKeyboardButton(text= 'Тренировка', callback_data='training')],
    #[InlineKeyboardButton(text= 'настройки', callback_data= 'settings')],
    [InlineKeyboardButton(text= 'Помощь', callback_data= 'help_info')]
])


lang = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Русский', callback_data='lang_ru')],
    [InlineKeyboardButton(text='Английский',callback_data= 'lang_en')],
    [InlineKeyboardButton(text='Назад',callback_data= 'backwards')]
])


again = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text= 'Создать карту', callback_data='add_card')],
    [InlineKeyboardButton(text= 'Тренировка', callback_data='training')],
    [InlineKeyboardButton(text= '🏠 Выйти в главное меню', callback_data='main_menu')],
])


back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back_to_language")]
])


repeat_training_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔁 Повторить тренировку", callback_data="repeat_training")],
    [InlineKeyboardButton(text="🏠 Закончить тренировку", callback_data="end_training")]
])


info_out = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text= '🏠 Выйти в главное меню', callback_data='main_menu')]
])