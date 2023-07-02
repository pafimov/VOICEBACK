from django.db import models
from .trimmer import trim, trim_audio
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.apps import apps
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Word(models.Model):
    word = models.CharField(max_length=30)
    word_start = models.FloatField()
    word_end = models.FloatField()
    sentence_start = models.FloatField()
    sentence_end = models.FloatField()
    full_video = models.CharField(max_length=100)
    film_name = models.CharField(max_length=100, default="Неизвестно")
    sentence_video = models.CharField(max_length=100, null=True, default=None)
    word_audio = models.CharField(max_length=100, null=True, default=None)
    accent = models.CharField(max_length=100, default="British")

    def check_sentence_video(self):
        if self.sentence_video != None and finders.find(self.sentence_video) != None:
            return
        path_to_static = apps.get_app_config('main').path + '/static/'
        new_name = 's' + str(self.pk) + '.mp4'
        new_path = path_to_static + new_name 
        trim(finders.find(self.full_video, all=False), new_path, self.sentence_start, self.sentence_end)
        self.sentence_video = new_name
        self.save()

    def check_word_audio(self):
        if self.word_audio != None and finders.find(self.word_audio) != None:
            return
        path_to_static = apps.get_app_config('main').path + '/static/'
        new_name = 'w' + str(self.pk) + '.mp3'
        new_path = path_to_static + new_name 
        trim_audio(finders.find(self.full_video, all=False), new_path, self.word_start, self.word_end)
        self.word_audio = new_name
        self.save()
    
    def check_all(self):
        self.check_sentence_video()
        self.check_word_audio()


class Detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(default=0)
