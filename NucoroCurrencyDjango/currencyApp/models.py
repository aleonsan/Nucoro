from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import requests

import itertools

# Create your models here.


class Provider(models.Model):
    name = models.CharField(db_index=True, max_length=100, unique=True)#This could be used as pk
    priority = models.IntegerField(db_index=True, validators=[MinValueValidator(0), MaxValueValidator(99)])

    api_url = models.URLField(help_text='Se ha considerado la fecha como endpoint a usar. Por lo tanto, la url sería del estilo: "http://data.fixer.io/api/"')
    access_key = models.SlugField(blank=True, null=True)
    
    def __str__(self):
        return self.name



class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        'Currency',
        related_name='exchanges',
        on_delete=models.CASCADE
    )
    exchanged_currency = models.ForeignKey(
        'Currency',
        related_name='exchanged_currency',
        on_delete = models.CASCADE
    )
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(
        db_index=True,
        decimal_places=6,
        max_digits=18
    )

    def get_exchange_rate_data(self, valuation_date, provider=None):#, exchanged_currency, source_currency
        CurrencyExchangeRate.objects.filter(valuation_date=valuation_date).delete()
        if provider:
            provider = Provider.objects.get(name)
        else:
            provider = Provider.objects.latest('priority')
        
        symbols_str = ''
        first = True
        currencies = Currency.objects.all()
        currencies_dict = {}
        for i in currencies:
            if first == True:
                symbols_str += i.code
                first = False
            else:
                symbols_str += ',' + i.code
            currencies_dict[i.code] = i

        api_query = {
            'symbols': symbols_str,
        }
        if provider.access_key:
            if provider.access_key != '':
                api_query['access_key'] = provider.access_key
        api_endpoint = provider.api_url + valuation_date.strftime('%Y-%m-%d')
        
        req = requests.get(api_endpoint, params=api_query)
        base = req.json()['base']
        base_currency = Currency.objects.get(code=base)
        rates = req.json()['rates']
        
        combinations = itertools.product(currencies_dict, repeat=2)
        exchange_rates_list = []
        for comb in combinations:
            currency_exchange_rate_dict = {
                'source_currency': currencies_dict[comb[0]],
                'exchanged_currency': currencies_dict[comb[1]],
                'valuation_date': valuation_date,
            }
            if comb[0] == comb[1]:
                currency_exchange_rate_dict['rate_value'] = 1
            elif comb[0] == base:
                currency_exchange_rate_dict['rate_value'] = rates[comb[1]]
            elif comb[1] == base:
                currency_exchange_rate_dict['rate_value'] = round(1/rates[comb[0]], 6)
            else:
                currency_exchange_rate_dict['rate_value'] = round(rates[comb[1]]/rates[comb[0]], 6)
            exchange_rates_list.append(CurrencyExchangeRate(**currency_exchange_rate_dict))

        CurrencyExchangeRate.objects.bulk_create(exchange_rates_list)



class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)#This could be used as pk
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.code




    
