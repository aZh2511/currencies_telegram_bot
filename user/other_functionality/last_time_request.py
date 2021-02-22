from database.db_commands import database
from datetime import datetime, timedelta


async def check_time():
    """Check if 10 minutes has passed."""
    now = datetime.now()
    last_request = await database.get_request_time()
    difference = timedelta(minutes=10)
    return (now - last_request) >= difference
