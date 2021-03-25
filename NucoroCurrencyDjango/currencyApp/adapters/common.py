from ..models import Currency, Provider, CurrencyExchangeRate


def _check_whole_data_in_database(source_currency, exchanged_currency, valuation_date):
    """ checks if all data is present in database """
    expected_rows = None  # calculate
    orm_rows = None  # calculate .count()
    return expected_rows == orm_rows


def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider=None):
    """ This is a decoupled from provider method that:gets data from specific adapters and transform it
        to be provided to views, or any other upper layer.
    """

    # here we could detect if we have all data in database:
    use_database = _check_whole_data_in_database(source_currency, exchanged_currency, valuation_date)
    if use_database:
        return Currency.objects.get(code=source_currency).exchanged_currency.filter(valuation_date)

    # select provider, latest in priority could be an option
    # a better approach would be try with each available in priority order
    # and return first that provides a proper result
    provider = provider or Provider.objects.latest('priority')

    # at this point this method for ALL providers should agreed / met an interface
    # BUT implementation would depend on each adapter
    provider_data = provider.adapter.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)

    # transform provider_data if needed to create ExchangeRate
    currency_exchange_rate = CurrencyExchangeRate.objects.create(provider_data)

    # return it directly or do any extra transformation if you like
    return currency_exchange_rate
