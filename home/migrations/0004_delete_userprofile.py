# Generated by Django 5.1.5 on 2025-03-07 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_destination_price_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
