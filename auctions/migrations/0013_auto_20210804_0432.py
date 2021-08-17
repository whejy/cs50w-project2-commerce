# Generated by Django 3.2.5 on 2021-08-04 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_watchlist_listing_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='listing_id',
            new_name='listingId',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='listing_id',
            new_name='listingId',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='start_bid',
            new_name='startBid',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='listing_id',
            new_name='listingId',
        ),
    ]