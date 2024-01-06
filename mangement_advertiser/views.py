from django.db.models import Func, Count
from django.db.models.functions import ExtractHour
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, TemplateView

from .form import AdForm
from .serializers import *


class RoundHour(Func):
    function = 'HOUR'
    template = "%(function)s(%(expressions)s)"


class GetClientIpMixin:
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ShowAdView(GetClientIpMixin, ListView):
    model = Advertiser
    template_name = 'ads.html'
    context_object_name = 'advertisers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advertisers = self.get_queryset()
        ads = []

        for advert in advertisers:
            approved_ads = advert.ads.filter(approve=True)
            ads.extend(approved_ads)

        ad_serializer = AdSerializer(ads, many=True)
        advertiser_serializer = AdvertiserSerializer(advertisers, many=True)

        context['advertisers'] = advertiser_serializer.data
        context['approved_ads'] = [(advert, advert.ads.filter(approve=True)) for advert in self.get_queryset()]
        context['ads'] = ad_serializer

        return context

    def get_queryset(self):
        advertisers = super().get_queryset()
        for advert in advertisers:
            ads = advert.ads.filter(approve=True)
            for ad in ads:
                View.objects.create(ad=ad, ip_address=self.get_client_ip(self.request))
        return advertisers


class AdClickView(GetClientIpMixin, CreateView):
    model = Click
    fields = []
    serializer_class = ClickSerializer

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs.get('pk')
        ad = get_object_or_404(Ad, pk=ad_id)

        click = Click(ad=ad, ip_address=self.get_client_ip(request))
        click.save()

        return redirect(ad.link)


class AdStatisticsView(TemplateView):
    template_name = 'ad_info.html'

    def get_context_data(self, unique_id_ad, **kwargs):
        context = super().get_context_data(**kwargs)

        ad = Ad.objects.get(unique_id_ad=unique_id_ad)

        clicks_per_hour = Click.objects.filter(ad=ad).annotate(
            hour=ExtractHour('click_time')
        ).values('hour').annotate(count=Count('id')).order_by('hour')

        views_per_hour = View.objects.filter(ad=ad).annotate(
            hour=ExtractHour('view_time')
        ).values('hour').annotate(count=Count('id')).order_by('hour')

        click_data = {entry['hour']: entry['count'] for entry in clicks_per_hour}
        view_data = {entry['hour']: entry['count'] for entry in views_per_hour}
        click_through_rates = []
        for hour, click_count in click_data.items():
            view_count = view_data.get(hour, 0)
            rate = click_count / view_count if view_count else 0
            click_through_rates.append({
                'hour': hour,
                'rate': rate,
                'click_count': click_count,
                'view_count': view_count,
            })

        click_times = Click.objects.filter(ad=ad).values_list('click_time', flat=True)
        view_times = View.objects.filter(ad=ad).values_list('view_time', flat=True)

        time_differences = [(view_time - click_time).total_seconds() for view_time, click_time in
                            zip(view_times, click_times)]
        average_time_difference = sum(time_differences) / len(time_differences) if time_differences else None

        serializer = AdStatisticsSerializer({
            'clicks_per_hour': [{'hour': entry['hour'], 'count': entry['count']} for entry in clicks_per_hour],
            'views_per_hour': [{'hour': entry['hour'], 'count': entry['count']} for entry in views_per_hour],
            'click_through_rates': click_through_rates,
            'average_time_difference': average_time_difference,
        })

        context = serializer.data
        return context


class CreateAdView(CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'create_ad.html'
    success_url = '/show_ad/'
