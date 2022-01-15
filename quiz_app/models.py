from django.db import models
from quiz.dto import *


class Choice(models.Model):
    uuid = models.SlugField(primary_key=True)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return self.text

class Question(models.Model):
        uuid = models.SlugField(primary_key=True)
        text = models.TextField()
        choices = models.ManyToManyField(Choice)

        class Meta:
            verbose_name = 'Вопрос'
            verbose_name_plural = 'Вопросы'

        def __str__(self):
            return self.text


class Quiz(models.Model):
    uuid = models.SlugField(primary_key=True)
    title = models.CharField(max_length=250)
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title




class Answer(models.Model):
    question_id = models.CharField(max_length=20, default='1')
    choices = models.ManyToManyField(Choice)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
         return self.question_id


class Answers(models.Model):
    quiz_uuid = models.CharField(max_length=20)
    answers = models.ManyToManyField(Answer)

    class Meta:
        verbose_name = 'Список Ответов'
        verbose_name_plural = 'Списки ответов'

    def __self__(self):
        return self.answers