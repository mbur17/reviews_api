from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.db import IntegrityError

from api_yamdb.api_yamdb.settings import CSV_FILES_DIR
from .models import Category, Genre, Title, GenreTitle, Review, Comment

import csv
import os

User = get_user_model()
FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'title': Title,
    'genretitle': GenreTitle,
    'review': Review,
    'comment': Comment,
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


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            print(f'загрузка таблицы {value.__qualname__}')


def open_csv(file_name):
    path = os.path.join(CSV_FILES_DIR, f'{file_name}.csv')
    try:
        with open(path, encoding='utf-8') as file:
            return list(csv.reader(file))
    except Exception as ex:
        print(ex)
        return




