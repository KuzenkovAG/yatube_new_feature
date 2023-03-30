from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    """Additional information about user."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Профиль'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Город',
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата Рождения',
    )
    photo = models.ImageField(
        'Аватар',
        upload_to='account/',
        blank=True,
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
