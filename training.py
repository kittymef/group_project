import random
import app.keyboards as kb
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from app.database.models import async_session, Word
from states import Training
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router()


#тренировка
@router.callback_query(lambda c: c.data == "training")
async def start_training(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    tg_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(Word).where(Word.tg_id == tg_id)
        )
        words = result.scalars().all()

    if len(words) < 4:
        await callback.message.answer("Добавь хотя бы 4 карточки, чтобы начать тренировку.")
        return

    correct_word = random.choice(words)
    wrong_words = random.sample([w for w in words if w.id != correct_word.id], 3)
    options = wrong_words + [correct_word]
    random.shuffle(options)

    # Сохраняет правильный ID в state
    await state.update_data(correct_id=correct_word.id, correct_answer=correct_word.translation)

    buttons = [
        [InlineKeyboardButton(text=w.translation, callback_data=f"answer_{w.id}")]
        for w in options
    ]
    await callback.message.answer(
        f"Выбери перевод слова: <b>{correct_word.word}</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode='HTML'
    )
    await state.set_state(Training.question)
    

#верно или нет  
@router.callback_query(Training.question)
async def check_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    correct_id = data.get("correct_id")
    correct_answer = data.get("correct_answer")

    chosen_id = int(callback.data.replace("answer_", ""))
    if chosen_id == correct_id:
        text = "✅ Верно!"
    else:
        text = f"❌ Неверно! Правильный ответ: <b>{correct_answer}</b>"

    await callback.message.answer(text, reply_markup=kb.repeat_training_kb, parse_mode="HTML")
        
    await state.clear()

    
#ф-ция для кнопки повтора
@router.callback_query(F.data == "repeat_training")
async def repeat_training(callback: CallbackQuery, state: FSMContext):
    await start_training(callback, state)


#ф-ция для кнопки домой
@router.callback_query(F.data == "end_training")
async def end_training(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🏠 Возвращаемся в главное меню.",
        reply_markup=kb.main)