from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class GolfClub(model_utils_models.TimeStampedModel):
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
        verbose_name=_('Line bot channel access token'),
        max_length=255,
        blank=True,
        null=True,
    )

    line_bot_channel_secret = models.CharField(
        verbose_name=_('Line bot channel secret'),
        max_length=64,
        blank=True,
        null=True,
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

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

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
