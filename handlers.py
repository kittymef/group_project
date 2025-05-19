from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import re
import app.keyboards as kb
import app.database.requests as rq
import aiosqlite

from states import WordInput
from training import router as training_router


router = Router()
#тут находятся все команды, некоторые из них спрятаны (например, создание модуля или настройка), они не являются
#обязательными для бота, поэтому их добавление, возможно, будет осуществлено позже


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет! Выбери, чем ты хочешь заняться.\n\n'
        #'<b>• Создать модуль</b> с несколькими карточками для заучивания\n'
        '<b>• Создать карточки</b>, не объединенные одной темой\n'
        '<b>• Потренироваться</b> с тобой\n\n'
        #'<b>Настройка</b> позволяет отредактировать твои карточки\n'
        'Если что-то непонятно, нажми <b>помощь</b>. Там все расписано подробно.',
                         reply_markup= kb.main,
                         parse_mode='HTML')
          
                         
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Если у тебя возникли вопросы или ты нашел(-а) баг, пожалуйста, свяжись с моим разработчиком. Написать можно в личные сообщения - @liebetrina')

    
@router.message(Command('info'))
async def get_info(message:Message):
    await message.answer('Этот бот разработан в рамках программы Цифровые Кафдры 2025. Благодаря этому проекту я оттачила навыки создания ботов, а вообще, я лингвист.) Надеюсь, что Меган поможет вам в изучении не только языка, но и любой другой информации, как она помогла когда-то мне полюбить программирование. Со временем Меган будет развиваться, пока что она выполняет только базовые функции бота.')
 
    
@router.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer('OK!')
    
    
@router.callback_query(F.data == 'add_card')
async def add_card(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('выбери язык для ввода', reply_markup= kb.lang)
 
    
@router.callback_query(F.data == 'help_info')
async def help_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Кнопка "Создать карту" позволяет создать пару для заучивания.\n'
                                     'Там ты можешь добавить слова с русского на английский и с английского на русский. После они будут доступны для тренировки.\n\n'
                                     'В тренировке ты можешь изучать введенные ранее слова.\n\n', 
    reply_markup= kb.info_out,
    parse_mode='HTML')


#фиксирует выбранный язык, запоминает слово    
@router.callback_query(F.data.startswith("lang_"))
async def process_lang_select(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    lang = callback_query.data.split("_")[1]
    await state.update_data(lang=lang)

    await callback_query.message.answer("Введи слово на выбранном языке:",
                                        reply_markup=kb.back)
    await state.set_state(WordInput.word)


#следит за тем, чтобы слово было введено на выбранном языке
@router.message(WordInput.word)
async def process_word_input(message: Message, state: FSMContext):
    user_word = message.text.strip()
    data = await state.get_data()
    lang = data.get("lang")

    if lang == "ru":
        if not re.fullmatch(r"[а-яА-ЯёЁ\s\-]+", user_word):
            await message.answer("❌ Пожалуйста, введите слово на русском языке.")
            return
    elif lang == "en":
        if not re.fullmatch(r"[a-zA-Z\s\-]+", user_word):
            await message.answer("❌ Пожалуйста, введите слово на английском языке.")
            return

    await state.update_data(word=user_word)
    await message.answer("Теперь введите перевод слова:")
    await state.set_state(WordInput.translation)


class WordInput(StatesGroup):
    word = State()
    translation = State()
  
    
@router.message(WordInput.word)
async def get_word(message: Message, state: FSMContext):
    await state.update_data(word=message.text.strip())
    await message.answer("Теперь введи перевод:",
                         reply_markup=kb.back)
    await state.set_state(WordInput.translation)


#сохраняет в БД через aiosqlite
@router.message(WordInput.translation)
async def get_translation(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    word = data["word"]
    translation = message.text.strip()
    lang = data["lang"]

   
    async with aiosqlite.connect("data.db") as db:
        await db.execute(
            "INSERT INTO words (tg_id, lang, word, translation) VALUES (?, ?, ?, ?)",
            (tg_id, lang, word, translation)
        )
        await db.commit()

    await message.answer("✅ Карточка добавлена! Хочешь добавить ещё — нажми «Создать карточки» снова.",
                         reply_markup= kb.again)
    await state.clear()
   
    
@router.callback_query(F.data == 'main_menu')
async def main_menu_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Вы вернулись в главное меню.", 
                            reply_markup= kb.main)
    await callback.answer()


#вызывает возврат на главное меню по инлайну    
@router.callback_query(F.data == 'backwards')
async def back_to_main_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Что вы хотите сделать?", reply_markup= kb.main)
    await callback.answer()


#выбирает язык по инлайну    
@router.callback_query(F.data == "back_to_language")
async def back_to_language_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите язык:", 
                                  reply_markup=kb.lang)
    await callback.answer()