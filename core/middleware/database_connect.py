import aiosqlite
from core.middleware.settings import DB_PATH


async def get_db_connection():
    return await aiosqlite.connect(DB_PATH)


# necessity of courotines below is a matter of discussion btw
async def init_reminder_dic():
    reminders = {}
    async with await get_db_connection() as db:
        data = await db.execute_fetchall("SELECT * FROM reminders")
    for i in data:
        reminders[i[0]] = i[1:]
    return reminders


async def set_reminder(chat_id, remind_time, message):
    async with await get_db_connection() as db:
        await db.execute('INSERT INTO reminders (chat_id, remind_time, message) VALUES (?, ?, ?)',
                         (chat_id, remind_time, message))
        await db.commit()


async def get_due_reminders(now):
    async with await get_db_connection() as db:
        cursor = await db.execute('SELECT id, chat_id, message FROM reminders WHERE remind_time <= ?', (now,))
        return await cursor.fetchall()


async def delete_reminder(reminder_id):
    async with await get_db_connection() as db:
        await db.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
        await db.commit()