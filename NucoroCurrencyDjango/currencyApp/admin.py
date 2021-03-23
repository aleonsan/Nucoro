from django.contrib import admin

from .models import *

# Register your models here.

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'symbol', )

admin.site.register(Currency, CurrencyAdmin)



class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_currency', 'exchanged_currency', 'valuation_date', 'rate_value', )
    list_filter = ('source_currency', 'exchanged_currency', 'valuation_date', )

admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)



class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_url', 'access_key', 'priority', )

admin.site.register(Provider, ProviderAdmin)