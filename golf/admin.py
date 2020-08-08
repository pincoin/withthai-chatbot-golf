from django.contrib import admin

from . import models


class GolfClubAdmin(admin.ModelAdmin):
    list_display = ('title_english', 'slug', 'phone', 'email')
    prepopulated_fields = {'slug': ('title_english',)}
    ordering = ['-created']


admin.site.register(models.GolfClub, GolfClubAdmin)
