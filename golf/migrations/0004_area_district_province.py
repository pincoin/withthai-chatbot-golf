# Generated by Django 3.1 on 2020-08-15 09:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0003_liff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Area english name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='Area Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='Area Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Province English name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='Province Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='Province Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.area', verbose_name='Location area')),
            ],
            options={
                'verbose_name': 'Province',
                'verbose_name_plural': 'Provinces',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='District English name')),
                ('title_thai', models.CharField(max_length=255, verbose_name='District Thai name')),
                ('title_korean', models.CharField(max_length=255, verbose_name='District Korean name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.province', verbose_name='Province')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
    ]
