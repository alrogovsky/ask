from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# ok, seichas


class Profile(models.Model):
    user = models.OneToOneField(User)
    rating = models.IntegerField(default=0)
    avatar_url = models.ImageField(max_length=60)


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


class Rate(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)