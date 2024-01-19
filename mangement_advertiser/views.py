from django.db.models import Func, Count
from django.db.models.functions import ExtractHour
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from kafka import KafkaProducer
from django.views import View
import json

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


class ShowAdView(GetClientIpMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        ads = self.get_queryset()

        for ad in ads:
            advertiser = ad.advertiser
            advertiser.views += 1
            advertiser.save()

        serialized_ads = AdSerializer(ads, many=True).data

        categorized_ads = {}
        for ad in serialized_ads:
            advertiser_id = ad['advertiser']['unique_id']
            if advertiser_id not in categorized_ads:
                categorized_ads[advertiser_id] = {
                    'advertiser': ad['advertiser'],
                    'ads': []
                }
            categorized_ads[advertiser_id]['ads'].append(ad)

        return Response(categorized_ads)

    def get_queryset(self):
        advertisers = Advertiser.objects.all()
        ads = []
        for advert in advertisers:
            approved_ads = advert.ads.filter(approve=True)
            ads.extend(approved_ads)
            for ad in approved_ads:
                View.objects.create(ad=ad, ip_address=self.get_client_ip(self.request))

                # kafka_producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
                # topic_name = 'ad_interactions'
                #
                # ad_interaction_data = {
                #     'ad_id': ad.id,
                #     'interaction_type': 'view',
                #     'advertiser_id': ad.advertiser.unique_id,
                # }
                #
                # kafka_producer.send(topic_name, json.dumps(ad_interaction_data).encode('utf-8'))

        return ads


class AdClickView(GetClientIpMixin, CreateView):
    permission_classes = [IsAuthenticated]

    model = Click
    fields = []
    serializer_class = ClickSerializer

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs.get('pk')
        ad = get_object_or_404(Ad, pk=ad_id)

        click = Click(ad=ad, ip_address=self.get_client_ip(request))
        advertiser = click.ad.advertiser
        advertiser.clicks += 1
        advertiser.save()
        click.save()

        # kafka_producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
        # topic_name = 'ad_interactions'
        #
        # ad_interaction_data = {
        #     'ad_id': ad.id,
        #     'interaction_type': 'click',
        #     'advertiser_id': ad.advertiser.unique_id,
        # }
        #
        # kafka_producer.send(topic_name, json.dumps(ad_interaction_data).encode('utf-8'))

        return redirect(ad.link)


class AdStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, unique_id_ad, **kwargs):
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

        serializer = AdStatisticsSerializer(data={
            'clicks_per_hour': [{'hour': entry['hour'], 'count': entry['count']} for entry in clicks_per_hour],
            'views_per_hour': [{'hour': entry['hour'], 'count': entry['count']} for entry in views_per_hour],
            'click_through_rates': click_through_rates,
            'average_time_difference': average_time_difference,
        })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class CreateAdView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateAdSerializer


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)


# ____________________________________________________________________________________________________
# generic view


class AdvertiserListCreateView(generics.ListCreateAPIView):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer


class AdvertiserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertiser.objects.all()
    serializer_class = AdvertiserSerializer


class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class ClickListCreateView(generics.ListCreateAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer


class ClickDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer


class ViewListCreateView(generics.ListCreateAPIView):
    queryset = View.objects.all()
    serializer_class = ViewSerializer


class ViewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = View.objects.all()
    serializer_class = ViewSerializer
