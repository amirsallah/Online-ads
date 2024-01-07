from rest_framework import serializers

from mangement_advertiser.models import *


class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    advertiser = AdvertiserSerializer()

    class Meta:
        model = Ad
        fields = '__all__'


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = '__all__'


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class AdStatisticsSerializer(serializers.Serializer):
    clicks_per_hour = serializers.ListField(child=serializers.DictField())
    views_per_hour = serializers.ListField(child=serializers.DictField())
    click_through_rates = serializers.ListField(child=serializers.DictField())
    average_time_difference = serializers.FloatField()
