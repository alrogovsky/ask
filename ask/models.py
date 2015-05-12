from django.db import models
from django.contrib.auth.models import User
import os
from ask_rogovsky2 import settings
# Create your models here.

# ok, seichas

uploads = "avatars"

class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    avatar_url = models.ImageField(
        upload_to = uploads,
        default = "/no-ava.jpg"
    )


class Tag(models.Model):
    word = models.CharField(max_length=15)


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=60)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)


class Answer(models.Model):
    author = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_right = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)


class Rate(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class Rate_Answer(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)


class Rate_Profile(models.Model):
    user = models.ForeignKey(User)
    profile = models.ForeignKey(Profile)