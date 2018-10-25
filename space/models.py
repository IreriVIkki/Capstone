from django.db import models
from django.contrib.auth.models import User
import math
from datetime import datetime
from django import forms


# Create your models here.


class Experiment(models.Model):
    random = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.random


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE, related_name='profile')
    user_name = models.CharField(max_length=50, null=True)
    d_pic = models.ImageField(
        upload_to='images/', blank=True, default='dwf_profile.jpg')
    coins = models.IntegerField(null=True)
    website = models.URLField(null=True)
    bio = models.TextField(null=True)

    @property
    def views(self):
        pass

    @property
    def badges(self):
        pass

    @property
    def rating(self):
        pass

    @classmethod
    def leader_board(cls):
        return cls.objects.all().order_by('-coins')
    # @classmethod
    # def new_user(cls):
    #     return cls.objects.last()

    @classmethod
    def create_profile(cls, user):
        cls.objects.create(user=user, user_name=user.username)

    @classmethod
    def update_coins(cls):
        pass

    # @property
    # def businesses(self):
    #     businesses = Business.objects.filter(owner=self)
    #     return businesses

    def save_profile(self, current_user):
        self.user = current_user
        self.save()

    def __str__(self):
        return self.user_name


class Question(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=140)
    question = models.TextField()
    date_asked = models.DateTimeField(auto_now_add=datetime.utcnow)
    answered = models.BooleanField(default=False)
    duplicate = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0, null=True)
    downvotes = models.IntegerField(default=0, null=True)
    views = models.IntegerField(default=0, null=True)

    def add_views(self):
        self.views += 1
        self.save()

    def save_question(self, author):
        self.author = author
        self.save()

    @classmethod
    def new_question(cls, author, title, question):
        cls.objects.create(author=author, title=title, question=question)

    @classmethod
    def all_questions(cls):
        return cls.objects.all()

    @property
    def votes(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, related_name='answers')
    answer = models.TextField()
    date_answered = models.DateTimeField(auto_now_add=datetime.utcnow)
    verified = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0, null=True)
    downvotes = models.IntegerField(default=0, null=True)
    views = models.IntegerField(default=0, null=True)

    @property
    def votes(self):
        return self.upvotes - self.downvotes

    def __str__(self):
        return self.author


class Task(models.Model):
    task = models.CharField(max_length=20, null=True)


class Checklist(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, null=True, related_name='tasks')
    item = models.CharField(max_length=100, null=True)


class CheckStatus(models.Model):
    status = models.BooleanField(default=False)
    label = models.OneToOneField(
        Checklist, null=True, on_delete=models.CASCADE, related_name='label')


class Announcement(models.Model):
    author = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='announcements')
    announcement = models.TextField()
    date_announced = models.DateTimeField(auto_now_add=datetime.utcnow)
