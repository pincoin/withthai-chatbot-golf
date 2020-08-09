from django.contrib import admin

from . import models


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'phone', 'email')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-created']


class LineUserAdmin(admin.ModelAdmin):
    list_display = ('line_user_id', 'follow_status', 'fullname')
    list_filter = ('follow_status',)
    ordering = ['-created']


admin.site.register(models.GolfClub, GolfClubAdmin)
admin.site.register(models.LineUser, LineUserAdmin)
