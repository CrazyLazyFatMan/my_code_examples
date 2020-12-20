import os

from django.conf import settings
from django.db import models


# Все примеры кода изъяты из контекста, так как проект, в котором они использовались, защищён NDA


class TimeStampedModel(models.Model):
    """Абстрактная модель с полями created и modified."""

    created = models.DateTimeField('Создано', auto_now_add=True)
    modified = models.DateTimeField('Изменено', auto_now=True)

    class Meta:
        abstract = True


class UploadCSVData(TimeStampedModel):
    """Модель загруженного для парсинга CSV,"""

    user = models.ForeignKey(verbose_name='Пользователь', to=User, on_delete=models.DO_NOTHING)
    success_parse = models.BooleanField(verbose_name='Обработан успешно', default=False)
    exception_text = models.TextField(
        verbose_name='Текст исключения',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.user} {self.created} {self.success_parse}'

    class Meta:
        verbose_name = 'Загруженный CSV файл'
        verbose_name_plural = 'Загруженные CSV файлы'


class AutoType(TimeStampedModel):
    """Модель `Типа` Авто."""

    name = models.CharField(verbose_name='Название типа ТС', max_length=255)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class AutoBrand(TimeStampedModel):
    """Модель `Бренда` Авто."""

    name = models.CharField(verbose_name='Название.', max_length=255)
    name_rus = models.CharField(verbose_name='Название (рус.)', blank=True, max_length=255, null=True)
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID')
    logo = models.ImageField(
        verbose_name='Логотип',
        upload_to=os.getenv('LOGO_PATH', '/logo'),
        blank=True,
    )
    is_popular = models.BooleanField(verbose_name='Популярный', default=False)
    with_credit_program = models.BooleanField(
        verbose_name='Можно в кредит',
        default=False,
    )
    car_type = models.ForeignKey(to=AutoType, verbose_name='Тип', blank=True, null=True,
                                 on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
