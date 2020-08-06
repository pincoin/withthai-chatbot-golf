from django.contrib import admin

from . import models


class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('created',)
    search_fields = ('request_body',)
    readonly_fields = ('request_header', 'request_body', 'created')
    ordering = ('-created',)


admin.site.register(models.WebhookRequestLog, WebhookLogAdmin)
