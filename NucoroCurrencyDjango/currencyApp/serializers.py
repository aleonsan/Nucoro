
from rest_framework import serializers

from .models import Currency, CurrencyExchangeRate

import datetime


class FilteredExchangeRateListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(valuation_date__range=(self.context['date_from'], self.context['date_to']), source_currency__code=self.context['source_currency'])
        return super(FilteredExchangeRateListSerializer, self).to_representation(data)



class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    exchanged_currency = serializers.StringRelatedField()
    source_currency = serializers.StringRelatedField()

    class Meta:
        model = CurrencyExchangeRate
        list_serializer_class = FilteredExchangeRateListSerializer
        fields = '__all__'



class CurrencyRatesSerializer(serializers.ModelSerializer):
    rates = CurrencyExchangeRateSerializer(source='exchanged_currency', many=True)
    
    def to_representation(self, instance):
        data = super(CurrencyRatesSerializer, self).to_representation(instance)
        
        result = {}
        for rate in data['rates']:
            if rate:
                result[rate['valuation_date']] = rate['rate_value']

        return { instance.code: result }
    
    class Meta:
        model = Currency
        fields = ['rates']