# Generated by Django 3.1 on 2020-08-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('golf', '0002_auto_20200826_2041'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineusermembership',
            options={'verbose_name': 'LINE user membership', 'verbose_name_plural': 'LINE user membership'},
        ),
        migrations.RemoveField(
            model_name='lineuser',
            name='golf_club',
        ),
        migrations.AddField(
            model_name='customergroup',
            name='line_users',
            field=models.ManyToManyField(db_index=True, through='golf.LineUserMembership', to='golf.CustomerGroup', verbose_name='LINE users'),
        ),
        migrations.AlterUniqueTogether(
            name='lineusermembership',
            unique_together={('customer_group', 'line_user')},
        ),
        migrations.RemoveField(
            model_name='lineusermembership',
            name='golf_club',
        ),
    ]
