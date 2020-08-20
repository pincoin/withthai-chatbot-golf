# Generated by Django 3.1 on 2020-08-20 01:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_auto_20200818_1758'),
    ]

    operations = [
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
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Season name')),
                ('season_start', models.DateField(verbose_name='Season start date')),
                ('season_end', models.DateField(verbose_name='Season end date')),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
            },
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title_english', models.CharField(max_length=255, verbose_name='Timeslot name')),
                ('slot_start', models.TimeField(verbose_name='Timeslot start time')),
                ('slot_end', models.TimeField(verbose_name='Timeslot end time')),
            ],
            options={
                'verbose_name': 'Timeslot',
                'verbose_name_plural': 'Timeslots',
            },
        ),
        migrations.AddField(
            model_name='golfclub',
            name='working_status',
            field=models.IntegerField(choices=[(0, 'Open'), (1, 'Closed'), (2, 'Suspended')], db_index=True, default=0, verbose_name='Working status'),
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Weekday'), (1, 'Weekend')], db_index=True, default=0, verbose_name='Day of week')),
                ('green_fee_list_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Green fee list price')),
                ('green_fee_selling_price', models.DecimalField(decimal_places=2, help_text='THB', max_digits=11, verbose_name='Green fee selling price')),
                ('customer_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.customergroup', verbose_name='Customer group')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.season', verbose_name='Season')),
                ('timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.timeslot', verbose_name='Timeslot')),
            ],
            options={
                'verbose_name': 'Service rate',
                'verbose_name_plural': 'Service rates',
            },
        ),
        migrations.AddField(
            model_name='customergroup',
            name='golf_club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='golf.golfclub', verbose_name='Golf club'),
        ),
    ]