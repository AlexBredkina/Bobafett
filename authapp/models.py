from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True, default=18)
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if now() < self.activation_key_expires:
            return False
        return True

    def __str__(self):
        return self.username

class ShopUserProfile(models.Model):

    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),

    )

    user = models.OneToOneField(User,unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(blank=True, max_length=255,verbose_name='тэги')
    about_me = models.CharField(blank=True, max_length=512, verbose_name='обо мне')
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=1, verbose_name='пол')

    @receiver(post_save, sender =User)
    def  create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user = instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()





