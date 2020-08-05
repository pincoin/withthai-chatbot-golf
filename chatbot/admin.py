from django.contrib import admin

from . import models


class WebhookLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.WebhookLog, WebhookLogAdmin)
