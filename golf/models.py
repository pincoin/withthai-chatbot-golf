import json
from pathlib import Path

from django.conf import settings
from django.db import models
from django.template.defaultfilters import time
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class Area(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
        verbose_name=_('Area english name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('Area Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('Area Korean name'),
        max_length=255,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return f'{self.title_english}'


class Province(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
        verbose_name=_('Province English name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('Province Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('Province Korean name'),
        max_length=255,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    area = models.ForeignKey(
        'golf.Area',
        verbose_name=_('Location area'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return f'{self.title_english}'


class District(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
        verbose_name=_('District English name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('District Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('District Korean name'),
        max_length=255,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    province = models.ForeignKey(
        'golf.Province',
        verbose_name=_('Province'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return f'{self.title_english}'


class GolfClub(model_utils_models.TimeStampedModel):
    WORKING_CHOICES = Choices(
        (0, 'open', _('Open')),
        (1, 'closed', _('Closed')),
        (2, 'suspended', _('Suspended')),
    )

    title_english = models.CharField(
        verbose_name=_('Golf club English name'),
        max_length=255,
        db_index=True,
    )

    title_thai = models.CharField(
        verbose_name=_('Golf club Thai name'),
        max_length=255,
        db_index=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    line_bot_channel_access_token = models.CharField(
        verbose_name=_('LINE bot channel access token'),
        max_length=255,
        blank=True,
        null=True,
    )

    line_bot_channel_secret = models.CharField(
        verbose_name=_('LINE bot channel secret'),
        max_length=64,
        blank=True,
        null=True,
    )

    line_notify_access_token = models.CharField(
        verbose_name=_('LINE notify access token'),
        max_length=64,
        blank=True,
        null=True,
    )

    info = models.JSONField(
        verbose_name=_('Course info'),
        blank=True,
        null=True,
    )

    business_hour_start = models.TimeField(
        verbose_name=_('Business hour start'),
    )

    business_hour_end = models.TimeField(
        verbose_name=_('Business hour end'),
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=32,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        blank=True,
        null=True,
    )

    fax = models.CharField(
        verbose_name=_('Fax number'),
        max_length=16,
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        max_length=255,
        blank=True,
        null=True,
    )

    district = models.ForeignKey(
        'golf.District',
        verbose_name=_('District'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    address = models.CharField(
        verbose_name=_('Golf club address'),
        max_length=255,
        blank=True,
        null=True,
    )

    latitude = models.DecimalField(
        verbose_name=_('Latitude'),
        max_digits=10,
        decimal_places=7,
        default=0,
    )

    longitude = models.DecimalField(
        verbose_name=_('Longitude'),
        max_digits=10,
        decimal_places=7,
        default=0,
    )

    liff = models.JSONField(
        verbose_name=_('LIFF'),
        blank=True,
        null=True,
    )

    scorecard = models.JSONField(
        verbose_name=_('Scorecard'),
        blank=True,
        null=True,
    )

    price_table = models.JSONField(
        verbose_name=_('Price table'),
        blank=True,
        null=True,
    )

    working_status = models.IntegerField(
        verbose_name=_('Working status'),
        choices=WORKING_CHOICES,
        default=WORKING_CHOICES.open,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def save(self, *args, **kwargs):
        if self.liff:
            with open(Path(settings.BASE_DIR) / 'liff' / 'static' / 'js' / 'liff' / 'json' / 'course.json') \
                    as json_file:
                self.info = json.load(json_file)

                self.info['header']['contents'][0]['text'] = self.title_english
                self.info['hero']['action']['uri'] = self.website
                self.info['body']['contents'][0]['contents'][1]['text'] = self.phone
                self.info['body']['contents'][1]['contents'][1]['text'] = self.fax
                self.info['body']['contents'][2]['contents'][1]['text'] = self.email
                self.info['body']['contents'][3]['contents'][1]['text'] \
                    = '{} - {}'.format(time(self.business_hour_start, 'H:i'), time(self.business_hour_end, 'H:i'))
                self.info['body']['contents'][4]['contents'][4]['action']['uri'] \
                    = f"https://liff.line.me/{self.liff['scorecard']['id']}"

        super(GolfClub, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title_english}'


class LineUser(model_utils_models.TimeStampedModel):
    FOLLOW_CHOICES = Choices(
        (0, 'unfollow', _('Unfollow')),
        (1, 'follow', _('Follow')),
    )

    line_user_id = models.CharField(
        verbose_name=_('LINE user ID'),
        max_length=48,
        db_index=True,
    )

    line_display_name = models.CharField(
        verbose_name=_('LINE display name'),
        max_length=128,
        blank=True,
    )

    follow_status = models.IntegerField(
        verbose_name=_('Follow status'),
        choices=FOLLOW_CHOICES,
        default=FOLLOW_CHOICES.follow,
        db_index=True,
    )

    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    fullname = models.CharField(
        verbose_name=_('Fullname'),
        max_length=32,
        blank=True,
    )

    class Meta:
        verbose_name = _('LINE user')
        verbose_name_plural = _('LINE users')

        unique_together = ('line_user_id', 'golf_club')

    def __str__(self):
        return f'{self.line_user_id}'


class CustomerGroup(model_utils_models.TimeStampedModel):
    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    title_english = models.CharField(
        verbose_name=_('Customer group name'),
        max_length=255,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Customer group')
        verbose_name_plural = _('Customer groups')

    def __str__(self):
        return f'{self.title_english}'


class Season(model_utils_models.TimeStampedModel):
    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    title_english = models.CharField(
        verbose_name=_('Season name'),
        max_length=255,
    )

    season_start = models.DateField(
        verbose_name=_('Season start date'),
    )

    season_end = models.DateField(
        verbose_name=_('Season end date'),
    )

    class Meta:
        verbose_name = _('Season')
        verbose_name_plural = _('Seasons')

    def __str__(self):
        return f'{self.title_english}-{self.season_start}-{self.season_end}'


class Timeslot(model_utils_models.TimeStampedModel):
    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    title_english = models.CharField(
        verbose_name=_('Timeslot name'),
        max_length=255,
    )

    day_of_week = models.IntegerField(
        verbose_name=_('Day of week'),
        choices=DAY_CHOICES,
        default=DAY_CHOICES.weekday,
        db_index=True,
    )

    slot_start = models.TimeField(
        verbose_name=_('Timeslot start time'),
    )

    slot_end = models.TimeField(
        verbose_name=_('Timeslot end time'),
    )

    class Meta:
        verbose_name = _('Timeslot')
        verbose_name_plural = _('Timeslots')

    def __str__(self):
        return f'{self.title_english}-{self.day_of_week}-{self.slot_start}-{self.slot_end}'


class Rate(model_utils_models.TimeStampedModel):
    customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Customer group'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    season = models.ForeignKey(
        'golf.Season',
        verbose_name=_('Season'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    timeslot = models.ForeignKey(
        'golf.Timeslot',
        verbose_name=_('Timeslot'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    green_fee_list_price = models.DecimalField(
        verbose_name=_('Green fee list price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    green_fee_selling_price = models.DecimalField(
        verbose_name=_('Green fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Service rate')
        verbose_name_plural = _('Service rates')
