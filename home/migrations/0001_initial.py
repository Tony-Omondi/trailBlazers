# Generated by Django 5.1.5 on 2025-03-06 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the destination (e.g., Nairobi National Park).', max_length=100)),
                ('description', models.TextField(help_text='A brief description of the destination.')),
                ('image', models.ImageField(blank=True, help_text='Image of the destination.', null=True, upload_to='destinations/')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the destination was added.')),
            ],
        ),
    ]
