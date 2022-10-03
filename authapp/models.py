from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/users', verbose_name='avatar')
    age = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Возраст')
    deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def __str__(self):
        return self.username

