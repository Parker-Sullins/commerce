# Generated by Django 3.1.7 on 2021-03-09 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210309_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active_listing',
            field=models.BooleanField(default=False),
        ),
    ]
