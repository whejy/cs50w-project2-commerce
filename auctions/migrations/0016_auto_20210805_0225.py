# Generated by Django 3.2.5 on 2021-08-05 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_watchlist_listing_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.IntegerField(blank=True),
        ),
    ]