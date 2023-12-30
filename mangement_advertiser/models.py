# models.py

from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=255)
    img_url = models.URLField(blank=True)
    link = models.URLField()
    unique_id_ad = models.IntegerField(primary_key=True)
    clicks_ad = models.IntegerField(default=0)
    views_ad = models.IntegerField(default=0)
    advertiser = models.ForeignKey('Advertiser', on_delete=models.CASCADE, related_name='ads')

    def __str__(self):
        return self.title

    def describe_me(self):
        return "This is the Ad class. It is used to store information about ads."

    def inc_clicks(self):
        self.clicks_ad += 1

    def inc_views(self):
        self.views_ad += 1

    def get_clicks(self):
        return self.clicks_ad

    def get_views(self):
        return self.views_ad
    def get_url(self):
        print(self.img_url.url)


class Advertiser(models.Model):
    name = models.CharField(max_length=255)
    unique_id = models.IntegerField(primary_key=True)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def describe_me(self):
        return "This is the Advertiser class. It is used to store information about advertisers."

    def inc_clicks(self):
        self.clicks += 1

    def inc_views(self):
        self.views += 1

    def get_clicks(self):
        return self.clicks

    def get_views(self):
        return self.views
