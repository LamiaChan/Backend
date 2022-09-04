from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from urllib.parse import urlparse
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from tinymce.models import HTMLField
from pytils.translit import slugify
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class NewsItem(models.Model):
    """
    Модель новостей
    """
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='news')
    body = HTMLField()
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

class Tag(models.Model):
    """
    Модель тегов
    """
    title = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.title)

class ContentType(models.Model):
    title = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.title)

class TranslatingStatus(models.Model):
    title = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.title)

class Manga(models.Model):
    """
    Модель манги
    """
    ru_title = models.CharField(max_length=256)
    eng_title = models.CharField(max_length=256, blank=True)
    jp_title = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    preview_image_url = models.ImageField(upload_to='manga')
    description = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag)
    updated = models.DateTimeField(default=datetime.now)
    year_of_publish = models.DateTimeField()
    likes = models.PositiveIntegerField(default=0)
    # Градиенты должны генерироваться автоматически с фронта при создании манги или ее редактировании
    gradient_color1 = models.CharField(default='empty', max_length=50)
    gradient_color2 = models.CharField(default='empty', max_length=50)
    content_type = models.ManyToManyField(ContentType)
    translating_status = models.ManyToManyField(TranslatingStatus)
    loaded_by_parser = models.BooleanField(default=True, editable=False)
    periodic_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Comic'
        verbose_name_plural = 'Comics'

    def save(self, *args, **kwargs):
        name = f'{slugify(self.ru_title)} check new chapters'
        if self.loaded_by_parser:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=10,
                period=IntervalSchedule.SECONDS,
            )

            task = PeriodicTask.objects.create(
                interval=schedule, 
                name=name,
                task='core.tasks.check_new_chapters',
                args=json.dumps(['arg1', 'arg2'])
            )
            self.periodic_task = task
        self.slug = slugify(self.ru_title)
        super(Manga, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.ru_title)

class Chapter(models.Model):
    """
    Модель Глав
    """
    title = models.CharField(max_length=256)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    translater = models.CharField(max_length=200, default='Неизвестно')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        bookmark_title = str(self.manga) + ' : ' + str(self.title)
        return str(bookmark_title)

class Page(models.Model):
    """
    Модель Страниц
    """
    number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='manga')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    
    def __str__(self):
        page_title = str(self.chapter) + ' - ' + str(self.number)
        return str(page_title)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель Юзера
    """
    #TODO
    #Нужно добавть ролей пользователям и переработать RANK_LIST
    #В зависемости от ролей юзер получает или не получает досуп к побликации манги
    # ВАЖНО публикация != загрузке
    username = models.CharField(_('user name'), max_length=50, unique=True)
    email = models.EmailField(_('email address'), max_length=30, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    user_image = models.ImageField(upload_to='upicks', null=True, blank=True)
    user_big_profile_image = models.ImageField(upload_to='upicks', null=True, blank=True)
    user_favorite_manga = models.ManyToManyField(Manga, blank=True, default=None)
    bookmarks = models.ManyToManyField(Page, blank=True, default=None)
    loved_tags = models.ManyToManyField(Tag, blank=True, default=None)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
    '''
    def email_user(self, subject, message, from_email=None, **kwargs):

        Sends an email to this User.

        send_mail(subject, message, from_email, [self.email], **kwargs)
    '''

class PageComment(models.Model):
    """
    Модель коментарии к странице
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
