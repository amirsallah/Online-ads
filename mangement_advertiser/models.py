from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from pip._internal.utils._jaraco_text import _


class AdUser(AbstractUser):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.TextField()

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions',
        related_query_name='user',
    )


class Ad(models.Model):
    title = models.CharField(max_length=255)
    img_url = models.URLField(blank=True)
    link = models.URLField()
    unique_id_ad = models.IntegerField(primary_key=True)
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE, related_name='ads')
    approve = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    click_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    view_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()


class Advertiser(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.IntegerField(primary_key=True)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AdHourlyStatistics(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    clicks = models.IntegerField()
    views = models.IntegerField()
    hour = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} - Clicks: {self.clicks}, Views: {self.views}, Hour: {self.hour}"


class AdDailyStatistics(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    clicks = models.IntegerField()
    views = models.IntegerField()
    day = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad} - Clicks: {self.clicks}, Views: {self.views}, Day: {self.day}"
