# _*_ coding: utf-8 _*_

from __future__ import unicode_literals

from django.db import models

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user_account = models.OneToOneField(User, on_delete = models.SET_NULL, null = True, blank = True, verbose_name = u"Пользователь")
    username = models.CharField(max_length=30, verbose_name = u"Username")
    avatar = models.CharField(max_length=200, verbose_name = u"Аватар")
    
    
    class Meta:
        verbose_name = u"Профиль"
        verbose_name_plural = u"Профили"
    
    def __unicode__(self):
        return self.username
        
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name = u"Название")
    
    class Meta:
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"
        
    def get_url(self):
        res = u"http://localhost/tag/{}/".format(self.name)
        return res
    
    def __unicode__(self):
        return self.name

class QuestionManager(models.Manager):
    def get_by_tag(self, tag):
        return self.filter(tags__name = tag)
        
    def get_by_id(self, question_id):
        return self.get(id = question_id)
        
    def get_new(self):
     return self.order_by('-date')[0:30]
     
    def get_hot(self):
        return sorted(self.all(),key=lambda a: -a.answer_count())
     
    
class AnswerManager(models.Manager):
    def get_by_question(self, question_object):
        return self.filter(question = question_object)
        
    def get_by_id(self, answer_id):
        return self.get(id = answer_id)
            

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name = u"Заголовок")
    date = models.DateTimeField(verbose_name = u"Дата")
    text = models.TextField(verbose_name = u"Текст")
    author = models.ForeignKey(UserProfile, verbose_name = u"Автор")
    tags = models.ManyToManyField(Tag, verbose_name = u"Теги")
    
    objects = QuestionManager()
    
    class Meta:
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"
        
    def get_url(self):
        res = u"http://localhost/question/{}/".format(self.id)
        return res
        
    def get_answers(self):
        return Answer.objects.get_by_question(self)
        
    def answer_count(self):
        return Answer.objects.get_by_question(self).count()
        
    def likes_count(self):
        return LikeQuestion.objects.filter(question=self, value=1).count()
        
    def dislikes_count(self):
        return LikeQuestion.objects.filter(question=self, value=0).count()
    
    def __unicode__(self):
        return self.title    

  
    
class Answer(models.Model):
    date = models.DateTimeField(verbose_name = u"Дата")
    text = models.TextField(verbose_name = u"Текст")
    author = models.ForeignKey(UserProfile, verbose_name = u"Автор")
    question = models.ForeignKey(Question, verbose_name = u"Вопрос")
    
    objects = AnswerManager()
    
    class Meta:
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"
        
    def likes_count(self):
        return LikeAnswer.objects.filter(answer=self, value=True).count()
        
    def dislikes_count(self):
        return LikeAnswer.objects.filter(answer=self, value=False).count()
        
    def user_liked(self, user):
        if LikeAnswer.objects.filter(answer = self, author = UserProfile.objects.get(user_account = user)).exists():
            user_like = LikeAnswer.objects.get(answer = self, author = UserProfile.objects.get(user_account = user))
            if user_like.value is True:
                return '1'
            else:
                return '-1'
        else:
            return '0'
    
    def __unicode__(self):
        return self.text
        
class LikeAnswer(models.Model):
    value = models.BooleanField(verbose_name = u"IsLike")
    answer = models.ForeignKey(Answer, verbose_name = u"Вопрос")
    author = models.ForeignKey(UserProfile,verbose_name = u"Пользователь")
    
    class Meta:
        verbose_name = u"Лайк ответа"
        verbose_name_plural = u"Лайки ответов"
    
    def __unicode__(self):
        return self.author.username
        
class LikeQuestion(models.Model):
    value = models.BooleanField(verbose_name = u"IsLike")
    question = models.ForeignKey(Question, verbose_name = u"Вопрос")
    author = models.ForeignKey(UserProfile,verbose_name = u"Пользователь")
    
    
    class Meta:
        verbose_name = u"Лайк вопроса"
        verbose_name_plural = u"Лайки вопросов"
    
    def __unicode__(self):
        return self.author.username
