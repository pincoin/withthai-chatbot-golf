from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class LiffAppInline(admin.TabularInline):
    model = models.LiffApp
    ordering = ['title', 'lang']
    extra = 1


class CustomerGroupInline(admin.TabularInline):
    model = models.CustomerGroup
    ordering = ['position', ]
    extra = 1


class SeasonInline(admin.TabularInline):
    model = models.Season
    ordering = ['season_start', ]
    extra = 1


class TimeslotInline(admin.TabularInline):
    model = models.Timeslot
    ordering = ['day_of_week', 'slot_start']
    extra = 1


class LineUserListInline(admin.TabularInline):
    model = models.CustomerGroup.line_users.through
    extra = 1


class GolfClubStaffListInline(admin.TabularInline):
    model = models.GolfClub.staffs.through
    raw_id_fields = ('user', 'golf_club')
    extra = 1


class GolfBookingOrderProductInline(admin.TabularInline):
    model = models.GolfBookingOrderProduct
    ordering = ['product', ]
    extra = 1


class GolfBookingOrderStatusLogtInline(admin.TabularInline):
    model = models.GolfBookingOrderStatusLog
    readonly_fields = ('order_status', 'payment_status', 'message',)
    ordering = ['-created', ]
    extra = 1


class HolidayAdmin(admin.ModelAdmin):
    list_display = ('title', 'holiday')
    date_hierarchy = 'holiday'
    ordering = ('-holiday',)


class AreaAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'title_thai', 'title_korean', 'position')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-position']


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'title_thai', 'title_korean', 'position')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-position']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'title_thai', 'title_korean', 'position')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-position']


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'phone', 'email', 'working_status')
    list_filter = ('district__province__title_english', 'working_status')
    prepopulated_fields = {'slug': ('title_english',)}
    raw_id_fields = ('customer_group',)
    readonly_fields = ('info_flex_message', 'order_flex_message', 'no_order_flex_message', 'liff')
    fieldsets = (
        (_('Golf club'), {
            'fields': ('title_english', 'title_thai', 'slug',
                       'hole', 'working_status', 'business_hour_start', 'business_hour_end',
                       'phone', 'email', 'fax', 'website', 'address', 'latitude', 'longitude', 'district',
                       'caddie_compulsory', 'cart_compulsory', 'min_pax', 'max_pax', 'customer_group',
                       'weekdays_min_in_advance', 'weekdays_max_in_advance',
                       'weekend_min_in_advance', 'weekend_max_in_advance',
                       'weekend_booking_on_monday', 'multiple_booking_orders',
                       'thumbnail', 'layout',)
        }),
        ('LINE', {
            'fields': ('line_bot_channel_access_token', 'line_bot_channel_secret', 'line_notify_access_token',
                       'info_flex_message', 'order_flex_message', 'no_order_flex_message',
                       'liff', 'scorecard', 'line_rich_menu')
        })
    )
    inlines = [LiffAppInline, CustomerGroupInline, SeasonInline, TimeslotInline, GolfClubStaffListInline]
    ordering = ['-created']


class LineUserAdmin(admin.ModelAdmin):
    list_display = ('line_user_id', 'fullname', 'email', 'phone', 'lang', 'line_display_name', 'follow_status')
    list_filter = ('follow_status',)
    # readonly_fields = ('line_user_id', 'line_display_name', 'golf_club', 'follow_status')
    ordering = ['-created']


class GreenFeeAdmin(admin.ModelAdmin):
    list_display = ('customer_group', 'season', 'timeslot', 'list_price', 'selling_price')
    list_filter = ('season__golf_club__title_english',)
    raw_id_fields = ('customer_group', 'season', 'timeslot')
    # form = forms.RateAdminForm


class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ('golf_club', 'title_english', 'category', 'position')
    list_display_links = ('golf_club', 'title_english',)
    list_filter = ('golf_club__title_english',)
    raw_id_fields = ('golf_club',)
    inlines = [LineUserListInline, ]
    ordering = ['golf_club', 'position']


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('golf_club', 'title_english', 'season_start', 'season_end')
    list_display_links = ('title_english',)
    list_filter = ('golf_club__title_english',)
    raw_id_fields = ('golf_club',)
    ordering = ['golf_club', 'season_start']


class TimeslotAdmin(admin.ModelAdmin):
    list_display = ('golf_club', 'title_english', 'day_of_week', 'slot_start', 'slot_end')
    list_display_links = ('title_english',)
    list_filter = ('golf_club__title_english',)
    raw_id_fields = ('golf_club',)
    ordering = ['golf_club', 'day_of_week', 'slot_start']


class GolfBookingOrderAdmin(admin.ModelAdmin):
    list_display = ('golf_club', 'fullname', 'round_date', 'round_time', 'pax', 'cart', 'total_selling_price',
                    'order_status', 'payment_status')
    list_display_links = ('golf_club', 'fullname')
    readonly_fields = ('user_agent', 'accept_language', 'ip_address', 'parent')
    list_filter = ('golf_club__title_english',)
    inlines = [GolfBookingOrderProductInline, GolfBookingOrderStatusLogtInline]
    date_hierarchy = 'round_date'
    ordering = ['-round_date', 'round_time']


class GolfBookingPromotionAdmin(admin.ModelAdmin):
    list_display = ('golf_club', 'title', 'promotion_start', 'promotion_end', 'active')
    list_filter = ('golf_club__title_english',)
    fieldsets = (
        (_('Promotion'), {
            'fields': ('golf_club', 'title', 'banner', 'promotion_start', 'promotion_end', 'active')
        }),
        (_('Promotion Conditions'), {
            'fields': ('condition_monday', 'condition_tuesday', 'condition_wednesday', 'condition_thursday',
                       'condition_friday', 'condition_saturday', 'condition_sunday', 'condition_holiday',
                       'condition_time_start', 'condition_time_end',
                       'condition_pax', 'condition_cart', 'condition_customer_group')
        }),
        (_('Discount'), {
            'fields': ('discount_fee', 'discount_method', 'discount_amount')
        }),
    )


admin.site.register(models.Holiday, HolidayAdmin)
admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.LineUser, LineUserAdmin)
admin.site.register(models.GreenFee, GreenFeeAdmin)
admin.site.register(models.CustomerGroup, CustomerGroupAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.Timeslot, TimeslotAdmin)
admin.site.register(models.GolfBookingOrder, GolfBookingOrderAdmin)
admin.site.register(models.GolfBookingPromotion, GolfBookingPromotionAdmin)
