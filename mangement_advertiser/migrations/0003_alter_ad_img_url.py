# Generated by Django 5.0 on 2023-12-30 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangement_advertiser', '0002_alter_ad_unique_id_ad_alter_advertiser_unique_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='img_url',
            field=models.URLField(blank=True),
        ),
    ]