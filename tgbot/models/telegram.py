from django.db import models


class User(models.Model):
    """Модель пользователя база"""
    cid = models.BigIntegerField('id telegram пользователя', unique=True)
    username = models.CharField('Username ТГ', max_length=40, blank=True, null=True)
    name = models.CharField('Имя ТГ', max_length=70, blank=True, null=True)
    lastname = models.CharField('Фамилия ТГ', max_length=70, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, )
    update_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True, )

    def __str__(self):
        return f'{self.cid} {self.username}'

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserAction(models.Model):
    cid = models.ForeignKey(User, verbose_name='Действие пользователя', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Наименование действия', max_length=100, blank=True, null=True)
    dop = models.TextField(verbose_name='Дополнительные параметры', blank=True, null=True)
    date_operation = models.DateTimeField(verbose_name='Дата действия', auto_now_add=True)

    class Meta:
        verbose_name = "Действие пользователя"
        verbose_name_plural = "Действия пользователей"


class Markup(models.Model):
    """ Модель кнопки """
    name = models.CharField(verbose_name='Имя переменной', max_length=50, null=True, unique=True)
    description = models.CharField(verbose_name='Краткое наименование', max_length=200, null=True)
    verbose = models.TextField(verbose_name='Текст кнопки')

    class Meta:
        verbose_name = "ТГ Кнопка"
        verbose_name_plural = "ТГ Кнопки"

    def __str__(self):
        return self.description


class Message(models.Model):
    """ Модель Сообщения """
    name = models.CharField(verbose_name='Имя переменной', max_length=50, null=True, unique=True)
    description = models.CharField(verbose_name='Краткое наименование', max_length=200, null=True)
    verbose = models.TextField(verbose_name='Текст сообщения')

    class Meta:
        verbose_name = "ТГ Сообщение"
        verbose_name_plural = "ТГ Сообщения"

    def __str__(self):
        return self.description
