# Generated by Django 3.1 on 2020-08-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='golfclub',
            name='line_bot_channel_access_token',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Line bot channel access token'),
        ),
    ]