class Adapter:

def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date)
    """ Here we could put specific code so no matter if connection is done via HTTP / websocket / 
        SFTP / any other TCP interface. For fixer we could just call their REST API.
    """

    # this code probably does not work, Ive just copy pasted from ExchangeRate model.
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

