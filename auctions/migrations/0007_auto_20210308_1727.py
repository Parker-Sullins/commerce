# Generated by Django 3.1.7 on 2021-03-08 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210308_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(default=None, max_length=45),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(default=None),
        ),
    ]
