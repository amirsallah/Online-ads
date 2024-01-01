from django.db import models
from django.utils import timezone


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
