import os
import time

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from ConnectID import settings
from ConnectID.choices import *


class FeedbackProject(models.Model):

    feedback = models.TextField()

    def __str__(self):
        return self.feedback


class Project(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, unique=True)
    abstract = models.TextField()
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    anonymity = models.BooleanField()
    visible = models.BooleanField(default=True)
    lookingFor = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=64, null=True)
    generalProjectType = models.CharField(max_length=32, choices=GENERAL_PROJECT_TYPES, null=True)
    projectType = models.CharField(max_length=32, choices=PROJECT_TYPES, null=True)
    projectStatus = models.CharField(max_length=6, choices=PROJECT_STATUS, null=True)
    projectWebsite = models.CharField(max_length=64, blank=True, null=True)
    location = models.CharField(max_length=4, choices=LOCATIONS, null=True)
    wiift = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        #db_table = 'keywords'       #TODO add keyword to database


'''
class ProjectTypeOptions(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    projectTypeOption_text = models.CharField(max_length=50)
    selected = models.IntegerField(default=0)
'''


def get_profilepicture_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'profilepictures/user_{0}.{1}'.format(instance.user.id, ext)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


# By default, only get profiles of users who are actual users
# If a superuser is made though manage.py, a Profile is automatically created and we don't want to see that
# The "hack" here is that the profile will have empty values only if created this way.
# Otherwise these fields need to be filled in
class ProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(headline="", bio="").exclude(headline=None, bio=None)


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.TextField(max_length=120, null=True)
    whyImHere = models.TextField(max_length=750, null=True)
    bio = models.TextField(max_length=4000, blank=True, null=True)
    linkedin = models.URLField(blank=True)
    profilePicture = models.ImageField(blank=True, storage=OverwriteStorage(), upload_to=get_profilepicture_path)
    favorites = models.ManyToManyField(Project)
    typeOfUser = models.CharField(max_length=32, choices=TYPE_OF_USER, null=True)
    website = models.CharField(max_length=64, blank=True, null=True)
    extraInfo = models.TextField(blank=True, null=True)
    # TODO add Expertise/background

    objects = ProfileManager()

    def get_favorites(self):
        return ",".join([str(p) for p in self.favorites.all()])

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @receiver(pre_delete, sender=User)
    def delete_chat(sender, instance, **kwargs):
        from chat.models import Conversation
        Conversation.objects.filter(participants=instance).delete()


def get_successstorypicture_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'successstories/projectpicture_{0}.{1}'.format(int(round(time.time() * 1000)), ext)


class SuccessStory(models.Model):
    title = models.CharField(max_length=64, unique=True)
    subtitle = models.CharField(max_length=128, unique=True)
    picture = models.ImageField(storage=OverwriteStorage(), upload_to=get_successstorypicture_path)
    website = models.URLField(null=True, blank=True)
    abstract = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Success Stories"