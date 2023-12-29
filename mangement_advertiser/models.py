from django.db import models


class BaseAdvertising:
    unique_id = models.IntegerField(primary_key=True)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def inc_clicks(self):
        self.clicks += 1

    def inc_views(self):
        self.views += 1

    def get_clicks(self):
        return self.clicks

    def get_views(self):
        return self.views

    def describe_me(self):
        return "This is the BaseAdvertising class. It is used to store information about ads and advertisers."

    def _check_unique_id(self):
        pass


class Advertiser(BaseAdvertising, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def describe_me(self):
        return "This is the Advertiser class. It is used to store information about advertisers."

    @staticmethod
    def get_total_clicks():
        total_clicks = 0
        advertisers = Advertiser.objects.all()
        for advertiser in advertisers:
            total_clicks += advertiser.get_clicks()
        return total_clicks

    @staticmethod
    def help():
        string = ""
        string += "id - The id of the advertiser.\n"
        string += "name - The name of the advertiser.\n"
        string += "clicks - The number of clicks the advertiser has.\n"
        string += "views - The number of views the advertiser has.\n"
        return string


class Ad(BaseAdvertising, models.Model):
    title = models.CharField(max_length=255)
    img_url = models.URLField()
    link = models.URLField()
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def describe_me(self):
        return "This is the Ad class. It is used to store information about ads."
