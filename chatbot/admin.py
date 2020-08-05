from django.contrib import admin

from . import models


class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('created',)
    search_fields = ('request_body', 'response_body')
    readonly_fields = ('request_header', 'request_body', 'response_header', 'response_body', 'created')
    ordering = ('-created',)


admin.site.register(models.WebhookLog, WebhookLogAdmin)
