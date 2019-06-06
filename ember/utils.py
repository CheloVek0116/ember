
"""
Файл для утилитарных скриптов
"""
from django.utils.text import slugify
from django.conf import settings
from django.db import models
from time import time


class LanguageField(models.CharField):

    """
    сниппет взят из https://www.djangosnippets.org/snippets/493/
    использует встроенные в джангу языки для создания LanguageField из CharField

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 5)
        kwargs.setdefault('choices', settings.LANGUAGES)

        super(LanguageField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return э


def gen_slug(slug):
    """
    генерация слага
    """
    slug = slugify(slug, allow_unicode=True)
    return '%s-%s' % (slug, str(int(time())))