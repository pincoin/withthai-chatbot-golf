from django.contrib import admin

from . import models


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
    list_display = ('title_english', 'slug', 'phone', 'email')
    list_filter = ('district__province__title_english',)
    prepopulated_fields = {'slug': ('title_english',)}
    readonly_fields = ('info',)
    inlines = [CustomerGroupInline, SeasonInline, TimeslotInline]
    ordering = ['-created']


class LineUserAdmin(admin.ModelAdmin):
    list_display = ('line_user_id', 'line_display_name', 'golf_club', 'follow_status', 'fullname')
    list_filter = ('follow_status', 'golf_club__title_english')
    readonly_fields = ('line_user_id', 'line_display_name', 'golf_club', 'follow_status')
    ordering = ['-created']


class RateAdmin(admin.ModelAdmin):
    list_display = ('customer_group', 'season', 'timeslot', 'green_fee_list_price', 'green_fee_selling_price')
    list_filter = ('season__golf_club__title_english',)
    raw_id_fields = ('customer_group', 'season', 'timeslot')
    # form = forms.RateAdminForm


admin.site.register(models.Area, AreaAdmin)
admin.site.register(models.Province, ProvinceAdmin)
admin.site.register(models.District, DistrictAdmin)
admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.LineUser, LineUserAdmin)
admin.site.register(models.Rate, RateAdmin)

admin.site.register(models.CustomerGroup)
admin.site.register(models.Season)
admin.site.register(models.Timeslot)
