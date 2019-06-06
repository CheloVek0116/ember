from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import AbstractUser


from ember.utils import LanguageField
from ember.utils import gen_slug
from django_countries.fields import CountryField

from django.utils import timezone
import urllib.parse


class User(AbstractUser):

    SEX_CHOICES = (

        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Not specified'),
    )

    avatar      = models.ImageField(blank=True, null=True)
    first_name  = models.CharField(max_length=50, verbose_name='Имя')
    last_name   = models.CharField(max_length=50, verbose_name='Фамилия')
    sex         = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Пол', default='N', blank=True, null=True)
    language    = LanguageField(max_length=50, verbose_name='Язык', blank=True, null=True)
    age         = models.PositiveIntegerField(blank=True, null=True)
    country     = CountryField(blank_label='Страна', blank=True, null=True)
    subscribers = models.ManyToManyField('User', blank=True, verbose_name='Подписчики', related_name='sub')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_page_url', kwargs={'username': self.username})

    class Meta:
        verbose_name = 'Прифиль'
        verbose_name_plural = 'Профили'


class Post(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, related_name='posts')
    slug      = models.SlugField(unique=True)
    content   = models.TextField(verbose_name='Контент')
    published = models.DateTimeField(
        auto_now_add=True, verbose_name='Опубликовано', db_index=True)
    
    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('blog:post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('blog:post_update_url', kwargs={'slug': self.slug})

    def save(self,*args, **kwargs):
        self.slug = gen_slug('post')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-published']


class Chat(models.Model):
    DIALOG = 'D'
    CHAT   = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, 'Dialog'),
        (CHAT, 'Chat')
    )

    type = models.CharField(
        ('Тип'),
        max_length = 1,
        choices    = CHAT_TYPE_CHOICES,
        default    = DIALOG,
    )

    members = models.ManyToManyField('User', verbose_name='Участник', related_name='member_chat')
 
    def get_absolute_url(self):
        return reverse('blog:dialog_detail_url', kwargs={'chat_id': self.pk })

 
class Message(models.Model):
    chat      = models.ForeignKey('Chat', verbose_name='Чат', on_delete=models.CASCADE, related_name='message_in_chat')
    author    = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='author_message')
    message   = models.TextField(verbose_name='Сообщение')
    pub_date  = models.DateTimeField(verbose_name='Дата сообщения', default=timezone.now)
    is_readed = models.BooleanField(verbose_name='Прочитано', default=False)
 
    class Meta:
        ordering = ['pub_date']
 
    def __str__(self):
        return self.message


'''@receiver(post_save, sender=User)
def signal_user(sender, instance, created, **kwargs):
    if created:
        login(instance)

@receiver(post_save, sender=Post)
def signal_post(sender, instance, created, **kwargs):
    if not created:
        return
    # отпавка письма 
    author = instance.blog.user.username
    subscribers = instance.blog.subscribers.all()
    recipients = []
    for sub in subscribers:
        if sub.email == '':
            continue
        else:
            recipients.append(sub.email)
    print(author, subscribers)
    message = 'У пользователя %s в блоге появилась новая запись!Ссылка:%s' % (author, 'http://127.0.0.1:8000/' + urllib.parse.unquote(instance.get_absolute_url()))
    print(message)
    subject = 'Новый пост'
    #email = EmailMessage(subject=subject, body=message, to=recipients)
    #email.send() '''