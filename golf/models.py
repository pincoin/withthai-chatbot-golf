import json
import uuid
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.template.defaultfilters import time
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


def upload_directory_path(instance, filename):
    return f"golf/{instance.slug}/{uuid.uuid4()}.{filename.split('.')[-1]}"


class Holiday(model_utils_models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_('Holiday name'),
        max_length=255,
    )

    holiday = models.DateField(
        verbose_name=_('Holiday day'),
        db_index=True,
        unique=True,
    )

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

    def __str__(self):
        return f'{self.title} {self.holiday}'


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
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
        (2, 'twentyseven', _('27 Holes')),
        (3, 'thirtysix', _('36 Holes')),
    )

    WORKING_CHOICES = Choices(
        (0, 'open', _('Course open')),
        (1, 'closed', _('Course closed')),
        (2, 'suspended', _('Suspended')),
    )

    CADDIE_COMPULSORY_CHOICES = Choices(
        (0, 'optional', _('Optional')),
        (1, 'compulsory', _('Compulsory')),
    )

    CART_COMPULSORY_CHOICES = Choices(
        (0, 'optional', _('Optional')),
        (1, 'compulsory', _('Compulsory')),
        (2, 'compulsory2', _('Compulsory 2 player+')),
        (3, 'compulsory3', _('Compulsory 3 player+')),
        (4, 'compulsory4', _('Compulsory 4 player+')),
        (5, 'compulsory5', _('Compulsory 5 player+')),
        (6, 'compulsory6', _('Compulsory 6 player+')),
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

    customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Default customer group'),
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        on_delete=models.SET_NULL,
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

    hole = models.IntegerField(
        verbose_name=_('No. of holes'),
        choices=HOLE_CHOICES,
        default=HOLE_CHOICES.eighteen,
        db_index=True,
    )

    min_pax = models.IntegerField(
        verbose_name=_('Min PAX'),
        default=1,
    )

    max_pax = models.IntegerField(
        verbose_name=_('Max PAX'),
        default=4,
    )

    weekdays_min_in_advance = models.IntegerField(
        verbose_name=_('Weekdays minimum in advance'),
        default=1,
        db_index=True,
    )

    weekdays_max_in_advance = models.IntegerField(
        verbose_name=_('Weekdays maximum in advance'),
        default=30,
        db_index=True,
    )

    weekend_min_in_advance = models.IntegerField(
        verbose_name=_('Weekend minimum in advance'),
        default=1,
        db_index=True,
    )

    weekend_max_in_advance = models.IntegerField(
        verbose_name=_('Weekend maximum in advance'),
        default=7,
        db_index=True,
    )

    weekend_booking_on_monday = models.BooleanField(
        verbose_name=_('Weekend booking on Monday'),
        default=False,
    )

    multiple_booking_orders = models.PositiveIntegerField(
        verbose_name=_('Multiple booking orders'),
        default=1,
    )

    caddie_compulsory = models.IntegerField(
        verbose_name=_('Caddie compulsory'),
        choices=CADDIE_COMPULSORY_CHOICES,
        default=CADDIE_COMPULSORY_CHOICES.compulsory,
        db_index=True,
    )

    cart_compulsory = models.IntegerField(
        verbose_name=_('Cart compulsory'),
        choices=CART_COMPULSORY_CHOICES,
        default=CART_COMPULSORY_CHOICES.optional,
        db_index=True,
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

    working_status = models.IntegerField(
        verbose_name=_('Working status'),
        choices=WORKING_CHOICES,
        default=WORKING_CHOICES.open,
        db_index=True,
    )

    thumbnail = models.ImageField(
        verbose_name=_('Thumbnail image'),
        upload_to=upload_directory_path,
        storage=default_storage,
        blank=True,
    )

    layout = models.ImageField(
        verbose_name=_('Layout image'),
        upload_to=upload_directory_path,
        storage=default_storage,
        blank=True,
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def save(self, *args, **kwargs):
        if self.liff:
            with open(Path(settings.BASE_DIR) / 'liff' / 'static' / 'js' / 'liff' / 'json' / 'course.json') \
                    as json_file:
                self.info = json.load(json_file)

                translation.activate('en')

                self.info['header']['contents'][0]['text'] = self.title_english
                self.info['hero']['action']['uri'] = self.website
                self.info['body']['contents'][0]['contents'][1]['text'] = self.get_hole_display()
                self.info['body']['contents'][1]['contents'][1]['text'] = self.phone
                self.info['body']['contents'][2]['contents'][1]['text'] = self.fax
                self.info['body']['contents'][3]['contents'][1]['text'] = self.email
                self.info['body']['contents'][4]['contents'][1]['text'] \
                    = '{} - {}'.format(time(self.business_hour_start, 'H:i'), time(self.business_hour_end, 'H:i'))
                self.info['body']['contents'][5]['contents'][4]['action']['uri'] \
                    = f"https://liff.line.me/{self.liff['scorecard']['id']}"

                translation.deactivate()

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
        unique=True,
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

    fullname = models.CharField(
        verbose_name=_('Fullname'),
        max_length=32,
        blank=True,
    )

    class Meta:
        verbose_name = _('LINE user')
        verbose_name_plural = _('LINE users')

    def __str__(self):
        return f'{self.line_user_id}'


class LineUserMembership(models.Model):
    line_user = models.ForeignKey(
        'golf.LineUser',
        verbose_name=_('LINE user'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Customer group'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('LINE user membership')
        verbose_name_plural = _('LINE user membership')


class CustomerGroup(model_utils_models.TimeStampedModel):
    MEMBER_CHOICES = Choices(
        (0, 'member', _('Member')),
        (1, 'member_guest', _('Member guest')),
        (2, 'visitor', _('Visitor')),
    )

    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    line_users = models.ManyToManyField(
        'golf.CustomerGroup',
        verbose_name=_('LINE users'),
        db_index=True,
        through='golf.LineUserMembership'
    )

    title_english = models.CharField(
        verbose_name=_('Customer group name'),
        max_length=255,
    )

    category = models.IntegerField(
        verbose_name=_('Member categories'),
        choices=MEMBER_CHOICES,
        default=MEMBER_CHOICES.visitor,
        db_index=True,
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

    caddie_fee_list_price = models.DecimalField(
        verbose_name=_('Caddie fee list price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    caddie_fee_selling_price = models.DecimalField(
        verbose_name=_('Caddie fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    cart_fee_list_price = models.DecimalField(
        verbose_name=_('Cart fee list price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    cart_fee_selling_price = models.DecimalField(
        verbose_name=_('Cart fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
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


class GreenFee(model_utils_models.TimeStampedModel):
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

    list_price = models.DecimalField(
        verbose_name=_('List price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    selling_price = models.DecimalField(
        verbose_name=_('Selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Green fee')
        verbose_name_plural = _('Green fee')


class GolfBookingOrder(model_utils_models.TimeStampedModel):
    ORDER_STATUS_CHOICES = Choices(
        (0, 'open', _('Booking open')),
        (1, 'confirmed', _('Booking confirmed')),
        (2, 'offered', _('Booking offered')),
        (3, 'accepted', _('Booking accepted')),
        (4, 'closed', _('Booking closed')),
    )

    PAYMENT_STATUS_CHOICES = Choices(
        (0, 'unpaid', _('Unpaid')),
        (1, 'paid', _('Paid')),
        (2, 'refund_requests', _('Refund requests')),
        (3, 'refunded', _('Refunded')),
    )

    order_no = models.UUIDField(
        verbose_name=_('Order no'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        db_index=True,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    line_user = models.ForeignKey(
        'golf.LineUser',
        verbose_name=_('LINE user'),
        db_index=True,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    fullname = models.CharField(
        verbose_name=_('Fullname'),
        max_length=64,
        blank=True,
    )

    customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Customer group'),
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    round_date = models.DateField(
        verbose_name=_('Round date'),
        db_index=True,
    )

    round_time = models.TimeField(
        verbose_name=_('Round time'),
        db_index=True,
    )

    pax = models.IntegerField(
        verbose_name=_('PAX'),
        default=1,
    )

    cart = models.IntegerField(
        verbose_name=_('Cart'),
        default=0,
    )

    user_agent = models.TextField(
        verbose_name=_('User-agent'),
        blank=True,
    )

    accept_language = models.TextField(
        verbose_name=_('Accept-language'),
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
        blank=True,
        null=True,
    )

    # Max = 999,999,999.99
    total_list_price = models.DecimalField(
        verbose_name=_('Total list price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    total_selling_price = models.DecimalField(
        verbose_name=_('Total selling price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent'),
        db_index=True,
        null=True,
        on_delete=models.CASCADE,
    )

    order_status = models.IntegerField(
        verbose_name=_('Order status'),
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_CHOICES.open,
        db_index=True,
    )

    payment_status = models.IntegerField(
        verbose_name=_('Payment status'),
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_CHOICES.unpaid,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Golf booking order')
        verbose_name_plural = _('Golf booking orders')

    def __str__(self):
        return f'{self.user} {self.total_selling_price} {self.created}'


class GolfBookingOrderProduct(model_utils_models.TimeStampedModel):
    PRODUCT_CHOICES = Choices(
        (0, 'green_fee', _('Green fee')),
        (1, 'caddie_fee', _('Caddie fee')),
        (2, 'cart_fee', _('Cart fee')),
    )

    order = models.ForeignKey(
        'golf.GolfBookingOrder',
        verbose_name=_('Golf booking order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Customer group'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    product = models.IntegerField(
        verbose_name=_('Product'),
        choices=PRODUCT_CHOICES,
        default=PRODUCT_CHOICES.green_fee,
        db_index=True,
    )

    # Max = 999,999,999.99
    list_price = models.DecimalField(
        verbose_name=_('List price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    selling_price = models.DecimalField(
        verbose_name=_('Selling price'),
        max_digits=11,
        decimal_places=2,
        default=Decimal('0.00'),
    )

    quantity = models.IntegerField(
        verbose_name=_('Quantity'),
        default=0,
    )

    @property
    def subtotal(self):
        return self.selling_price * self.quantity

    @property
    def list_price_subtotal(self):
        return self.list_price * self.quantity

    class Meta:
        verbose_name = _('Golf booking order product')
        verbose_name_plural = _('Golf booking order products')

    def __str__(self):
        return f'order - {self.order.order_no} / product - {self.get_product_display()}'


class GolfBookingOrderStatusLog(model_utils_models.TimeStampedModel):
    order = models.ForeignKey(
        'golf.GolfBookingOrder',
        verbose_name=_('Golf booking order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        db_index=True,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    order_status = models.IntegerField(
        verbose_name=_('Order status'),
        choices=GolfBookingOrder.ORDER_STATUS_CHOICES,
        default=GolfBookingOrder.ORDER_STATUS_CHOICES.open,
        db_index=True,
    )

    payment_status = models.IntegerField(
        verbose_name=_('Payment status'),
        choices=GolfBookingOrder.PAYMENT_STATUS_CHOICES,
        default=GolfBookingOrder.PAYMENT_STATUS_CHOICES.unpaid,
        db_index=True,
    )

    message = models.TextField(
        verbose_name=_('Message'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Golf booking order status log')
        verbose_name_plural = _('Golf booking order status logs')

    def __str__(self):
        return f'{self.message} at {self.created}'


class GolfBookingPromotion(model_utils_models.TimeStampedModel):
    DISCOUNT_FEE_CHOICES = Choices(
        (0, 'green_fee', _('Green fee')),
        (1, 'caddie_fee', _('Caddie fee')),
        (2, 'cart_fee', _('Cart fee')),
        (3, 'total', _('Total amount')),
    )

    DISCOUNT_METHOD_CHOICES = Choices(
        (0, 'percent', _('Percent')),
        (1, 'minus', _('Minus')),
        (2, 'assign', _('Assign')),
    )

    golf_club = models.ForeignKey(
        'golf.GolfClub',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        verbose_name=_('Promotion title'),
        max_length=255,
    )

    promotion_start = models.DateField(
        verbose_name=_('Promotion start date'),
    )

    promotion_end = models.DateField(
        verbose_name=_('Promotion end date'),
    )

    active = models.BooleanField(
        verbose_name=_('Promotion active'),
        default=True,
    )

    condition_monday = models.BooleanField(
        verbose_name=_('Monday condition'),
        blank=True,
        null=True,
    )

    condition_tuesday = models.BooleanField(
        verbose_name=_('Tuesday condition'),
        blank=True,
        null=True,
    )

    condition_wednesday = models.BooleanField(
        verbose_name=_('Wednesday condition'),
        blank=True,
        null=True,
    )

    condition_thursday = models.BooleanField(
        verbose_name=_('Thursday condition'),
        blank=True,
        null=True,
    )

    condition_friday = models.BooleanField(
        verbose_name=_('Friday condition'),
        blank=True,
        null=True,
    )

    condition_saturday = models.BooleanField(
        verbose_name=_('Saturday condition'),
        blank=True,
        null=True,
    )

    condition_sunday = models.BooleanField(
        verbose_name=_('Sunday condition'),
        blank=True,
        null=True,
    )

    condition_holiday = models.BooleanField(
        verbose_name=_('Holiday condition'),
        blank=True,
        null=True,
    )

    condition_time_start = models.TimeField(
        verbose_name=_('Time start condition'),
        blank=True,
        null=True,
    )

    condition_time_end = models.TimeField(
        verbose_name=_('Time end condition'),
        blank=True,
        null=True,
    )

    condition_pax = models.IntegerField(
        verbose_name=_('PAX condition'),
        blank=True,
        null=True,
    )

    condition_cart = models.IntegerField(
        verbose_name=_('Cart condition'),
        blank=True,
        null=True,
    )

    condition_customer_group = models.ForeignKey(
        'golf.CustomerGroup',
        verbose_name=_('Customer group condition'),
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.CASCADE,
    )

    discount_fee = models.IntegerField(
        verbose_name=_('Discount fee'),
        choices=DISCOUNT_FEE_CHOICES,
        default=DISCOUNT_FEE_CHOICES.green_fee,
        db_index=True,
    )

    discount_method = models.IntegerField(
        verbose_name=_('Discount method'),
        choices=DISCOUNT_METHOD_CHOICES,
        default=DISCOUNT_METHOD_CHOICES.percent,
        db_index=True,
    )

    discount_amount = models.DecimalField(
        verbose_name=_('Discount amount'),
        max_digits=10,
        decimal_places=7,
        default=0,
    )

    class Meta:
        verbose_name = _('Golf booking promotion')
        verbose_name_plural = _('Golf booking promotions')

    def __str__(self):
        return f'{self.title}'
