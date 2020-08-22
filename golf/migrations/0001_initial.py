# Generated by Django 3.1 on 2020-08-22 12:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='CustomerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Customer group name')),
                ('position', models.IntegerField(db_index=True, default=0, verbose_name='Position')),
            ],
            options={
                'verbose_name': 'Customer group',
                'verbose_name_plural': 'Customer groups',
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
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='GolfClub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(db_index=True, max_length=255, verbose_name='Golf club English name')),
                ('title_thai', models.CharField(db_index=True, max_length=255, verbose_name='Golf club Thai name')),
                ('slug', models.SlugField(allow_unicode=True, help_text='A short label containing only letters, numbers, underscores or hyphens for URL', max_length=255, unique=True, verbose_name='Slug')),
                ('line_bot_channel_access_token', models.CharField(blank=True, max_length=255, null=True, verbose_name='LINE bot channel access token')),
                ('line_bot_channel_secret', models.CharField(blank=True, max_length=64, null=True, verbose_name='LINE bot channel secret')),
                ('line_notify_access_token', models.CharField(blank=True, max_length=64, null=True, verbose_name='LINE notify access token')),
                ('info', models.JSONField(blank=True, null=True, verbose_name='Course info')),
                ('business_hour_start', models.TimeField(verbose_name='Business hour start')),
                ('business_hour_end', models.TimeField(verbose_name='Business hour end')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('fax', models.CharField(blank=True, max_length=16, null=True, verbose_name='Fax number')),
                ('website', models.URLField(blank=True, max_length=255, null=True, verbose_name='Website')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Golf club address')),
                ('latitude', models.DecimalField(decimal_places=7, default=0, max_digits=10, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=7, default=0, max_digits=10, verbose_name='Longitude')),
                ('caddie_compulsory', models.IntegerField(choices=[(0, 'Optional'), (1, 'Compulsory')], db_index=True, default=1, verbose_name='Caddie compulsory')),
                ('cart_compulsory', models.IntegerField(choices=[(0, 'Optional'), (1, 'Compulsory'), (2, 'Compulsory 2 player+'), (3, 'Compulsory 3 player+'), (4, 'Compulsory 4 player+'), (5, 'Compulsory 5 player+'), (6, 'Compulsory 6 player+')], db_index=True, default=0, verbose_name='Cart compulsory')),
                ('liff', models.JSONField(blank=True, null=True, verbose_name='LIFF')),
                ('scorecard', models.JSONField(blank=True, null=True, verbose_name='Scorecard')),
                ('working_status', models.IntegerField(choices=[(0, 'Open'), (1, 'Closed'), (2, 'Suspended')], db_index=True, default=0, verbose_name='Working status')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.district', verbose_name='District')),
            ],
            options={
                'verbose_name': 'Golf club',
                'verbose_name_plural': 'Golf clubs',
            },
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Timeslot name')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
                ('slot_start', models.TimeField(verbose_name='Timeslot start time')),
                ('slot_end', models.TimeField(verbose_name='Timeslot end time')),
                ('golf_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.golfclub', verbose_name='Golf club')),
            ],
            options={
                'verbose_name': 'Timeslot',
                'verbose_name_plural': 'Timeslots',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Season name')),
                ('season_start', models.DateField(verbose_name='Season start date')),
                ('season_end', models.DateField(verbose_name='Season end date')),
                ('caddie_fee_list_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee list price')),
                ('caddie_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Caddie fee selling price')),
                ('cart_fee_list_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee list price')),
                ('cart_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Cart fee selling price')),
                ('golf_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.golfclub', verbose_name='Golf club')),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
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
            name='GreenFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('list_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='List price')),
                ('selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Selling price')),
                ('customer_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.customergroup', verbose_name='Customer group')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.season', verbose_name='Season')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.timeslot', verbose_name='Timeslot')),
            ],
            options={
                'verbose_name': 'Green fee',
                'verbose_name_plural': 'Green fee',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.province', verbose_name='Province'),
        ),
        migrations.AddField(
            model_name='customergroup',
            name='golf_club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.golfclub', verbose_name='Golf club'),
        ),
        migrations.CreateModel(
            name='LineUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('line_user_id', models.CharField(db_index=True, max_length=48, verbose_name='LINE user ID')),
                ('line_display_name', models.CharField(blank=True, max_length=128, verbose_name='LINE display name')),
                ('follow_status', models.IntegerField(choices=[(0, 'Unfollow'), (1, 'Follow')], db_index=True, default=1, verbose_name='Follow status')),
                ('fullname', models.CharField(blank=True, max_length=32, verbose_name='Fullname')),
                ('golf_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.golfclub', verbose_name='Golf club')),
            ],
            options={
                'verbose_name': 'LINE user',
                'verbose_name_plural': 'LINE users',
                'unique_together': {('line_user_id', 'golf_club')},
            },
        ),
    ]
