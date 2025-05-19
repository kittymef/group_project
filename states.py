# states.py
from aiogram.fsm.state import StatesGroup, State


class Training(StatesGroup):
    question = State()
 
    
class WordInput(StatesGroup):
    word = State()
    translation = State()