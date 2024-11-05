from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from api_yamdb.api_yamdb.settings import CSV_FILES_DIR
from .models import Category, Genre, Title, GenreTitle, Review, Comment

import csv
import os

User = get_user_model()
FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'review': Review,
    'comments': Comment,
    'users': User
}
FIELDS = {
    'category': {
        'category': Category
    },
    'title_id': {
        'title': Title
    },
    'genre_id': {
        'genre': Genre
    },
    'author': {
        'author': User
    },
    'review_id': {
        'review': Review
    }
}


def change_foreign_values(data_csv: dict):
    """
    Изменяет значения внешних ключей в словаре данных.
    Параметры: data_csv (dict): Словарь с данными из CSV-файла.
    Возвращает: dict: Словарь с измененными значениями внешних ключей.
    """
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            data_csv_copy[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file: str, class_name):
    """
    Загружает данные из CSV-файла в указанную модель.
    Параметры:
        file (str): Имя CSV-файла без расширения.
        class_name (Model): Модель Django, в которую будут загружены данные.
    Возвращает:
        None
    """
    data = open_csv(file)
    rows = data[1:]
    for row in rows:
        data = dict(zip(data[0], row))
        data = change_foreign_values(data)
        try:
            table = class_name(**data)
            table.save()
        except Exception as ex:
            print(
                f'возникла ошибка {ex} при загрузке '
                f'таблицы {class_name.__qualname__}')
            break
    print(f'таблица {class_name.__qualname__}')


class Command(BaseCommand):
    """
    Команда для загрузки данных из CSV-файлов в базу данных.
    Используется для инициализации базы данных данными из файлов.
    """
    def handle(self, *args, **options):
        """
        Основной метод для выполнения команды.
        """
        for key, value in FILES_CLASSES.items():
            print(f'загрузка таблицы {value.__qualname__}')
            load_csv(key, value)


def open_csv(file_name):
    """
    Открывает и читает данные из CSV-файла.
    Параметры:
        file_name (str): Имя CSV-файла без расширения.
    Возвращает:
        list: Список строк из CSV-файла или None в случае ошибки.
    """
    path = os.path.join(CSV_FILES_DIR, f'{file_name}.csv')
    try:
        with open(path, encoding='utf-8') as file:
            return list(csv.reader(file))
    except Exception as ex:
        print(ex)
        return




