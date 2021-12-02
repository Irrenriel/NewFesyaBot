from aiogram.dispatcher.filters.state import StatesGroup, State


class ExampleState(StatesGroup):
    First = State()
    Second = State()