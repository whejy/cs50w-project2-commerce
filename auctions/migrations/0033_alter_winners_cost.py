# Generated by Django 3.2.5 on 2021-08-12 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_winners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winners',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
