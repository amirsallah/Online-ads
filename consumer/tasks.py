import json

from celery import shared_task
from kafka import KafkaConsumer

from mangement_advertiser.models import Ad, Advertiser


@shared_task
def process_kafka_messages():
    kafka_consumer = KafkaConsumer(
        'ad_interactions',
        bootstrap_servers='127.0.0.1:9092',
        group_id='ad_interaction_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in kafka_consumer:
        ad_interaction_data = message.value

        ad_id = ad_interaction_data['ad_id']
        interaction_type = ad_interaction_data['interaction_type']
        advertiser_id = ad_interaction_data['advertiser_id']

        ad = Ad.objects.get(id=ad_id)

        advertiser = Advertiser.objects.get(unique_id=advertiser_id)
        cost = calculate_cost(ad, interaction_type)
        advertiser.budget -= cost
        advertiser.save()


def calculate_cost(ad, interaction_type):
    if interaction_type == 'click':
        return ad.cost_per_click
    elif interaction_type == 'view':
        return ad.cost_per_view
    else:
        return 0
