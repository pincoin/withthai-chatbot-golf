# Generated by Django 3.1 on 2020-08-06 04:01

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Message log',
                'verbose_name_plural': 'Message logs',
            },
        ),
        migrations.CreateModel(
            name='WebhookRequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('request_header', models.JSONField(blank=True, verbose_name='Request header')),
                ('request_body', models.JSONField(blank=True, verbose_name='Request body')),
            ],
            options={
                'verbose_name': 'Webhook request log',
                'verbose_name_plural': 'Webhook request logs',
            },
        ),
        migrations.DeleteModel(
            name='WebhookLog',
        ),
    ]
