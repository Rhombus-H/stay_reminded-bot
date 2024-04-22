from typing import List

WEEKDAYS = {'понедельник': 'monday',
            'вторник': 'tuesday',
            'среда': 'saturday',
            'четверг': 'thursday',
            'пятница': 'friday',
            'суббота': 'saturday',
            'воскресенье': 'sunday'
            }

WEEKDAYS_SHORTENED = {'понедельник': 'ПН',
                      'вторник': 'ВТ',
                      'среда': 'СР',
                      'четверг': 'ЧТ',
                      'пятница': 'ПТ',
                      'суббота': 'СБ',
                      'воскресенье': 'ВС'}


def translate(period: str) -> str:
    translated_period = []
    for i in period.lower().split(', '):
        translated_period.append(WEEKDAYS[i])
    return ','.join(translated_period)


def shorten(period: str) -> str:
    shortened_period = []
    for i in period.lower().split(',, '):
        shortened_period.append(WEEKDAYS_SHORTENED[i])
    return ', '.join(shortened_period)