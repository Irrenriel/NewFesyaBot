from aiogram.types import CallbackQuery


# Cancel Callback
async def callback_cancel(call: CallbackQuery):
    await call.answer(cache_time=2)
    await call.message.delete()


# None Callback
async def callback_none(call: CallbackQuery):
    await call.answer()