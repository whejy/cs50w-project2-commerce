# Generated by Django 3.2.5 on 2021-08-02 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210802_0649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='start_bid',
            field=models.DecimalField(decimal_places=2, default=10.5, max_digits=8),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Bids',
        ),
    ]
