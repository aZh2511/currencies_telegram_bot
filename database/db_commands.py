from datetime import datetime

from aiogram import types
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from loader import db


class DBCommands:
    """Class for working with DB."""
    pool: Connection = db

    ADD_NEW_USER = "INSERT INTO users (chat_id, username, full_name, adding_date) " \
                   "VALUES ($1, $2, $3, $4)"
    COUNT_USERS = "SELECT COUNT (*) FROM users"
    GET_USERS = "SELECT (username, full_name) FROM users"
    ADD_CURRENCY = "UPDATE currency SET value=$1 WHERE currency=$2"
    GET_CURRENCIES = "SELECT (currency, value) FROM currency"
    GET_ID_REQUEST = "SELECT id FROM last_request"
    GET_TIME_REQUEST = "SELECT adding_date FROM last_request"
    ADD_LAST_REQUEST = "UPDATE last_request SET adding_date=$1 WHERE id=$2"

    async def add_new_user(self):
        """Add new user to db."""
        user = types.User.get_current()
        command = self.ADD_NEW_USER

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        adding_date = datetime.now()

        args = chat_id, username, full_name, adding_date

        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def count_users(self):
        """Count users in db."""
        command = self.COUNT_USERS
        record = await self.pool.fetchval(command)
        return record

    async def get_users(self):
        """Get all users from the db."""
        command = self.GET_USERS
        data = await self.pool.fetch(command)

        data = [data[i][0] for i in range(len(data))]

        text = ''
        for num, row in enumerate(data):
            text += f'{num + 1}. @{row[0]} {row[1]}\n'
        return text

    async def add_currencies(self, data: dict):
        """Update currencies data in db."""
        command = self.ADD_CURRENCY

        for key in data:
            await self.pool.fetchval(command, data.get(key), key)

    async def get_id_request(self):
        """Get the id of last request."""
        command = self.GET_ID_REQUEST
        currency_id = await self.pool.fetchval(command)
        return currency_id

    async def add_last_request(self):
        """Update the last request time."""
        command = self.ADD_LAST_REQUEST
        now = datetime.now()
        request_id = await self.get_id_request()

        return await self.pool.fetchval(command, now, request_id)

    async def get_request_time(self):
        """Get the time of last request."""
        command = self.GET_TIME_REQUEST
        return await self.pool.fetchval(command)

    async def get_currency(self):
        """Get currency rates."""
        command = self.GET_CURRENCIES

        data = await self.pool.fetch(command)

        text = ''
        for row in data:
            text += f'{row[0][0]}: {round(row[0][1], 2)}\n'
        return text


database = DBCommands()
