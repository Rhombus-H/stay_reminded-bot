from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    # ReplyKeyboardRemove,
)


def reminders_list(reminders):
    keyboard = []
    for j in range(len(reminders)):
        reminder = reminders[j]
        keyboard.append([
            KeyboardButton(
                text=' '.join(reminder),
                callback_data=f'reminder_{j}')])
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )


def files_list(file_data):
    keyboard = []
    for j in range(len(file_data)):
        file_name = file_data[j][1]
        file_id = file_data[j][0]
        keyboard.append([
            InlineKeyboardButton(
                text=file_name,
                callback_data=file_id
            )
        ])
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
        resize_keyboard=True
    )


main_table = [
    [InlineKeyboardButton(
        text='📅 Установить напоминалку',
        callback_data='set_reminder'),
        InlineKeyboardButton(
            text='🗑 Удалить напоминалку',
            callback_data='delete_reminder')],
    [InlineKeyboardButton(
        text='💾 Добавить материал',
        callback_data='add_file'),
        InlineKeyboardButton(
            text='🗑 Удалить материал',
            callback_data='delete_file')],
    [InlineKeyboardButton(
        text='📄 Список материалов',
        callback_data='list_files'),
        InlineKeyboardButton(
            text='📋 Список напоминалок',
            callback_data='list_reminders')],
    [InlineKeyboardButton(
        text='⚙️ Настроить часовой пояс',
        callback_data='set_timezone'),
        InlineKeyboardButton(
            text='📚 Помощь',
            callback_data='bot_help')]
]
# file_choice_table = [
#     [InlineKeyboardButton(
#         text='Загрузить фото',
#         callback_data='add_photo'),
#      InlineKeyboardButton(
#         text='Загрузить видео',
#         callback_data='add_video')],
#     [InlineKeyboardButton(
#         text='Загрузить документ',
#         callback_data='add_document'),
#      InlineKeyboardButton(
#         text='Загрузить аудио',
#         callback_data='add_audio')]
# ]

time_zones_table = []
for i in range(-11, 13):
    time_zones_table.append(
        [InlineKeyboardButton(text=f'UTC+{i}', callback_data=f'tz_{i}')]
    )
main_table = InlineKeyboardMarkup(
    inline_keyboard=main_table,
    one_time_keyboardone_time_keyboard=True)

# file_choice_table = InlineKeyboardMarkup(
#     inline_keyboard=file_choice_table,
#     one_time_keyboardone_time_keyboard=True)
iclose_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(
        text='Выйти в меню',
        callback_data='close_keyboard')]]
)
