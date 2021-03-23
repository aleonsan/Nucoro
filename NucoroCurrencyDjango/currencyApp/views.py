from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.views import View

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Currency, CurrencyExchangeRate
from .serializers import *

from datetime import datetime, timedelta, date
from decimal import Decimal
import random
import json

# Create your views here.


def index(request):
    return HttpResponse('Hola Mundo')


@api_view(['GET'])
def mockdata(request, year, month, day):
    if request.method == 'GET':
        if 'symbols' in request.GET:
            if request.GET['symbols'].find(',') > 0:
                symbols = request.GET['symbols'].split(',')
            else:
                symbols = [request.GET['symbols']]
            date_str = str(year) + '-' + str(month) + '-' + str(day)

            result = {
                'date': date_str,
                'base': 'EUR',
                'rates': {},
            }

            for i in Currency.objects.all():
                if i.code != 'EUR' and i.code in symbols:
                    result['rates'][i.code] = Decimal(random.randrange(200000, 3000000))/1000000
                elif i.code == 'EUR' and i.code in symbols:
                    result['rates']['EUR'] = 1

            return Response(result)
        else:
            return HttpResponseNotFound('Not Found')



class timeseries(APIView):
    def get(self, request, format=None):
        if all(i in self.request.GET for i in ['source_currency', 'date_from', 'date_to']):
            if len(Currency.objects.filter(code=request.GET['source_currency'])) > 0:
                queryset = CurrencyExchangeRate.objects.filter(valuation_date__range=(self.request.GET['date_from'], self.request.GET['date_to']), source_currency__code=self.request.GET['source_currency']).exclude(exchanged_currency__code=self.request.GET['source_currency']).order_by('valuation_date')

                start_date = datetime.strptime(self.request.GET['date_from'], '%Y-%m-%d')
                end_date = datetime.strptime(self.request.GET['date_to'], '%Y-%m-%d')

                exchanged_currencies = Currency.objects.exclude(code=self.request.GET['source_currency'])
                delta = timedelta(days=1)

                if len(queryset) != len(exchanged_currencies) * ((end_date - start_date).days + 1):
                    while start_date <= end_date:
                        date_check = True
                        for i in exchanged_currencies:
                            if not queryset.filter(valuation_date=start_date, exchanged_currency=i):
                                CurrencyExchangeRate().get_exchange_rate_data(start_date)
                                break

                        start_date += delta

                results = {}
                for i in exchanged_currencies:
                    results[i.code] = {}
                    for j in queryset.filter(exchanged_currency=i):
                        results[i.code][j.valuation_date.strftime('%Y-%m-%d')] = j.rate_value

                return Response(results)
            
            else:
                return HttpResponseNotFound('source_currency does not exist')
        else:
            return HttpResponseNotFound('Parameters source_currency, date_from and date_to are needed')



class timeseries2(generics.ListAPIView):
    def get_queryset(self):
        if all(i in self.request.GET for i in ['source_currency', 'date_from', 'date_to']):
            return Currency.objects.exclude(code=self.request.GET['source_currency'])
        else:
            return None

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CurrencyRatesSerializer(queryset, many=True, context=self.request.GET)
        return Response(serializer.data)



class calculator(APIView):
    def get(self, request, format=None):
        if all(i in self.request.GET for i in ['source_currency', 'amount', 'exchanged_currency']):
            if len(Currency.objects.filter(code=request.GET['source_currency'])) > 0 and len(Currency.objects.filter(code=request.GET['exchanged_currency'])) > 0:
                today_date = date.today()
                exchange_rate = CurrencyExchangeRate.objects.filter(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=today_date)
                
                if len(exchange_rate) == 0:
                    CurrencyExchangeRate().get_exchange_rate_data(today_date)
                    exchange_rate = CurrencyExchangeRate.objects.get(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=today_date)
                else:
                    exchange_rate = exchange_rate[0]
                
                results = {
                    'source_currency': exchange_rate.source_currency.code,
                    'source_currency_amount': Decimal(request.GET['amount']),
                    'exchanged_currency': exchange_rate.exchanged_currency.code,
                    'exchanged_currency_amount': Decimal(request.GET['amount']) * exchange_rate.rate_value,
                }

                return Response(results)
            else:
                return HttpResponseNotFound('source_currency or exchanged_currency do not exist')
        
        else:
            return HttpResponseNotFound('Parameters source_currency, amount and exchanged_currency are needed')
        


class time_weighted_rate(APIView):
    def get(self, request, format=None):
        if all(i in self.request.GET for i in ['source_currency', 'start_date', 'amount', 'exchanged_currency']):
            if len(Currency.objects.filter(code=request.GET['source_currency'])) > 0 and len(Currency.objects.filter(code=request.GET['exchanged_currency'])) > 0:
                start_date = datetime.strptime(self.request.GET['start_date'], '%Y-%m-%d')
                today_date = date.today()

                initial_rate = CurrencyExchangeRate.objects.filter(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=start_date)
                final_rate = CurrencyExchangeRate.objects.filter(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=today_date)

                if len(initial_rate) == 0:
                    CurrencyExchangeRate().get_exchange_rate_data(start_date)
                    initial_rate = CurrencyExchangeRate.objects.get(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=start_date).rate_value
                else:
                    initial_rate = initial_rate[0].rate_value
                if len(final_rate) == 0:
                    CurrencyExchangeRate().get_exchange_rate_data(today_date)
                    final_rate = CurrencyExchangeRate.objects.get(source_currency__code=request.GET['source_currency'], exchanged_currency__code=request.GET['exchanged_currency'], valuation_date=today_date).rate_value
                else:
                    final_rate = final_rate[0].rate_value
                
                twr = initial_rate/final_rate-1

                return Response({
                    'source_currency': request.GET['source_currency'],
                    'exchange_currency': request.GET['exchanged_currency'],
                    'initial_rate': initial_rate,
                    'final_rate': final_rate,
                    'twr': twr,
                })
            
            else:
                return HttpResponseNotFound('source_currency or exchanged_currency do not exist')
        else:
            return HttpResponseNotFound('Parameters source_currency, amount, exchanged_currency and start_date are needed')



class backoffice(View):
    currencies = Currency.objects.all()
    custom_context = {
            'currencies': currencies,
            'date_today': date.today().strftime('%Y-%m-%d'),
        }

    def get(self, request):
        return render(request, 'backoffice.html', context=self.custom_context)

    def post(self, request):
        if request.FILES:
            mock_data = json.loads(request.FILES['mockdata'].read())
            rates = mock_data['rates']
            exchanged_currencies = Currency.objects.exclude(code=mock_data['base'])

            results = {'results': {}}
            for currency in exchanged_currencies:
                results['results'][currency.code] = {}
                for valuation_date in rates:
                    if currency.code in rates[valuation_date]:
                        results['results'][currency.code][valuation_date] = rates[valuation_date][currency.code]
            
            context = {**self.custom_context, **results}

            return render(request, 'backoffice.html', context=context)
            
        else:
            return render(request, 'backoffice.html', context=self.custom_context)
