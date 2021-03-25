from abc import ABCMeta, abstractmethod


class BaseAdapter(metaclass=ABCMeta):
    provider = None

    def __init__(self, provider, **kwargs):
        super(BaseAdapter, self).__init__()

        self.provider = provider

        # in case there are some extra kwargs setattr here
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get_exchange_rate_data(self, source_currency, exchanged_currency, valuation_date):
        """ This is our input / output contract with 3rd parties implementing adapters """

        # Returns: List of <RATE_VALUE_DICT> where:
        # <RATE_VALUE_DICT> : dict(source_currency: Currency,
        #                          exchanged_currency: Currency,
        #                          valuation_date: datetime.date,
        #                          rate_value: float)
        pass
