from typing import List

WEEKDAYS = {'понедельник': 'monday',
            'вторник': 'tuesday',
            'среда': 'saturday',
            'четверг': 'thursday',
            'пятница': 'friday',
            'суббота': 'saturday',
            'воскресенье': 'sunday'
            }


def translate(period: str) -> str:
    translated_period = []
    for i in period.lower().split():
        translated_period.append(WEEKDAYS[i])
    return ','.join(translated_period)