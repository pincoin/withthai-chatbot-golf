from django.contrib import admin

from . import models


class GolfClubAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.GolfClub, GolfClubAdmin)
