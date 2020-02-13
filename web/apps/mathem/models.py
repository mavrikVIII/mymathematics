from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Question(models.Model):
    question_title=models.CharField('название вопроса', max_length=200)
    question_text=models.TextField('название вопроса')
    answer_text=models.IntegerField('ответ')


    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name='Вопрос'
        verbose_name_plural='Вопросы'

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    author_name = models.CharField('Имя автора комментария',max_length=50)
    comment_text = models.CharField('Текст комментария',max_length=200)
    pub_date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

# обратная связь по задаче
class PeoplesErrors(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    people_name = models.CharField('Имя или ник автора сообщения', max_length=50)
    people_message=models.TextField('Текст его сообщения',max_length=200)
    date_message = models.DateTimeField('Дата сообщения')

    def __str__(self):
        return self.people_name

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural='Ошибки'
