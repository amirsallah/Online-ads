from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


class Ad(models.Model):
    title = models.CharField(max_length=255)
    img_url = models.URLField(blank=True)
    link = models.URLField()
    unique_id_ad = models.IntegerField(primary_key=True)
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE, related_name='ads')
    approve = models.BooleanField(default=False)

    # cost_type_choices = [
    #     ('CPM', 'Cost Per Mille (CPM)'),
    #     ('CPC', 'Cost Per Click (CPC)'),
    # ]
    # cost_type = models.CharField(max_length=3, choices=cost_type_choices, default='CPM')
    # cost_per_mille = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # cost_per_click = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

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
