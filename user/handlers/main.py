from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from database.db_commands import database
from loader import dp, bot
from ..other_functionality import get_currency, check_time, get_exchange, draw


@dp.message_handler(commands=['start'], state='*')
async def starting(message: types.Message, state: FSMContext):
    """Process /start command."""
    await database.add_new_user()
    text = 'Welcome to online-currency bot!\n/list - get list of rates.\n' \
           '/exchange 10 USD to EUR - calculate exchange\n/history USD/EUR for 7 days - history of exchange rate'

    await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['list'])
async def list_currencies(message: types.Message):
    """Send a list of available currencies."""
    text = 'Available currencies (based on USD)\n'

    if await check_time():
        await database.add_last_request()

        data = get_currency()
        await database.add_currencies(data)
        for key in data:
            text += f'{key}: {round(data.get(key), 2)}\n'
    else:
        data = await database.get_currency()
        text += data

    await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    """Send the exchange rate."""
    text = get_exchange(message.text)

    await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['history'])
async def exchange(message: types.Message):
    """Send the graph."""
    if not draw(message.text):
        await message.answer('No exchange rate data is available for the selected currency.')
    else:
        photo = InputFile('media/graph.png')

        await bot.send_photo(chat_id=message.from_user.id, photo=photo)
