from django.contrib import admin
from . import models


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('date', 'code', 'value', 'change', 'change_percent', 'source')

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.ExchangeRate, ExchangeRateAdmin)
