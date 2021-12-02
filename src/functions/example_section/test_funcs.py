from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from resources.tools.states import ExampleState


async def test(mes: Message, state: FSMContext):
    if await state.get_state() == 'ExampleState:First':
        text = 'Going to None state!'
        await state.finish()
    else:
        text = 'Going to ExampleState.First state!'
        await ExampleState.First.set()

    await mes.answer(text)