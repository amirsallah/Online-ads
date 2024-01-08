from datetime import datetime, timedelta

from celery import shared_task
from django.db.models import Sum

from .models import Click, View, Ad, AdHourlyStatistics, AdDailyStatistics


@shared_task
def calculate_hourly_statistics():
    start_time = datetime.now() - timedelta(hours=1)
    end_time = datetime.now()

    ads = Ad.objects.all()

    for ad in ads:
        clicks_per_hour = Click.objects.filter(ad=ad, click_time__range=(start_time, end_time)).count()
        views_per_hour = View.objects.filter(ad=ad, view_time__range=(start_time, end_time)).count()

        ad_hourly_statistics = AdHourlyStatistics(ad=ad, clicks=clicks_per_hour, views=views_per_hour)
        ad_hourly_statistics.save()

        print(f"Ad ID: {ad.id}, Clicks: {clicks_per_hour}, Views: {views_per_hour}, Hour: {datetime.now()}")


@shared_task
def calculate_daily_statistics_from_hourly():
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)

    ads = Ad.objects.all()

    for ad in ads:
        clicks_per_hour = AdHourlyStatistics.objects.filter(
            ad=ad, hour__range=(start_time, end_time)
        ).aggregate(Sum('clicks'))['clicks__sum'] or 0

        views_per_hour = AdHourlyStatistics.objects.filter(
            ad=ad, hour__range=(start_time, end_time)
        ).aggregate(Sum('views'))['views__sum'] or 0

        ad_daily_statistics = AdDailyStatistics(ad=ad, clicks=clicks_per_hour, views=views_per_hour,
                                                day=start_time.date())
        ad_daily_statistics.save()
