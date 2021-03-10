# Generated by Django 3.1.7 on 2021-03-09 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20210309_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing_id',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.listing'),
        ),
        migrations.DeleteModel(
            name='ClosedBid',
        ),
    ]