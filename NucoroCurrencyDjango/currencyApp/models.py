from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import requests

import itertools

# Create your models here.


class Provider(models.Model):
    # code is a better approach to match entities han name as it can define a strict format
    code = models.CharField(max_length=60, unique=True)
    # This could bejus representation layer data
    name = models.CharField(db_index=True, max_length=100)
    priority = models.IntegerField(db_index=True, validators=[MinValueValidator(0), MaxValueValidator(99)])

    # Here we might like to provide a field specifying adapter path
    # (where provider adapter submodule is implemented)
    # in this approach we choose a fixed subpath as preferred approach as the
    # field could have length retrictions
    adapter_path = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.name

    @property
    def adapter(self):
        """ This is only sugar to be able to do provider_instance.adapter in your views code """
        return self._get_adapter()

    def _get_adapter(self, adapter_path=None):
        """ Here your adapter is imported and injected into your entity
            Depending on your policy you could choose between:
            1. inject adapter as external parameter "adapter_path" (its kind of odd)
            2. get provider's path field (could have restrictions if field is not model properly) 
            3. infere adapter_path from your provider's code
        """
        # this code should be cleaner/more resilient and placed into a mixin that would be injected in your model(s)
        # that can use adapters. This is just a draft to understand the idea, so no prob with that.
        _adapter_path = (adapter_path
                         or self.adapter_path
                         or 'adapters.{}.adapter'.format(self.code))

        try:
            _adapter_module = __import__(_adapter_path, fromlist=['adapter'])

            # any extra context could be passed
            extra_context = {}
            return getattr(_adapter_module, 'Adapter')(**extra_context)

        except ImportError as e:
            msg = f'Can not import adapter from {_adapter_path}: {e}'
        except AttributeError as e:
            msg = f'Adapter from {_adapter_path} has not a proper Adapter structure: {e}'

        # you would decide what to do here, more common behavior would be raise a custom Exception
        logger.error(msg)
        # raise NucoroException(msg)


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

    # removed from here method "get_exchange_rate_data" as it wouldnt be the scope / responsability
    # of this model. A better and decoupled place would be:
    # - something like adapters/common if we would like to inject provider dependency.
    # - into provider method (if not coupled to certain implementation)




class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)#This could be used as pk
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.code




    
