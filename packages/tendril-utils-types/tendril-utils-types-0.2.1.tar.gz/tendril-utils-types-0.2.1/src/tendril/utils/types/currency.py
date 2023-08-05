# Copyright (C) 2015 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Currency Types (:mod:`tendril.utils.types.currency`)
====================================================

The :mod:`tendril.utils.types.currency` contains classes which allow for easy
use and manipulation of currency values. The primary focus is on the primary
use cases of Currencies within tendril, i.e. :

- Handling foreign exchange conversions and exchange rates in application code
  without too much fuss.
- Handling currency arithmetic and comparisons.

This module uses a specific `Base Currency`, defined by
:const:`tendril.config.BASE_CURRENCY` and
:const:`tendril.config.BASE_CURRENCY_SYMBOL` and available as this module's
:data:`native_currency_defn` module variable. In case this module is
to be used independent of Tendril, at least those configuration options
*must* be defined in :mod:`tendril.config`.

.. rubric:: Module Contents

.. autosummary::

    native_currency_defn
    CurrencyDefinition
    CurrencyValue

.. seealso:: :mod:`tendril.utils.types`, for an overview applicable to most
             types defined in Tendril.

.. todo:: The core numbers in this module need to switched to
          :class:`decimal.Decimal`.

"""

from cachecontrol.heuristics import ExpiresAfter

from tendril.config import BASE_CURRENCY
from tendril.config import BASE_CURRENCY_SYMBOL
from tendril.config import BASE_CURRENCY_NAME
from tendril.config import BASE_CURRENCY_LANG
from tendril.config import FIXER_IO_API_KEY

from tendril.utils import www
from decimal import Decimal
from numbers import Number
from num2words import num2words

from .unitbase import NumericalUnitBase
from .unitbase import Percentage

# TODO Switch to a heuristic which uses a cached value only if a fresh
# one is not available.
requests_session = www.get_session(heuristic=ExpiresAfter(days=5))


class CurrencyDefinition(object):
    """
    Instances of this class define a currency.

    The minimal requirement to define a currency is a :attr:`code`, which
    would usually be a standard internationally recognized currency code.

    In addition to the :attr:`code`, a currency definition also includes
    an optional :attr:`symbol`, which is used to create string representations
    of currency values in that currency. In the absence of a :attr:`symbol`,
    the :attr:`code` is used in it's place.

    Unless otherwise specified during the instantiation of the class,
    the exchange rate is obtained from internet services by the
    :meth:`_get_exchval` method.

    :param code: Standard currency code.
    :param symbol: Symbol to use to represent the currency. Optional.
    :param exchval: Exchange rate to use, if not automatic. Optional.

    """
    def __init__(self, code, symbol=None, name=None, exchval=None, lang='en'):
        self._code = code
        self._symbol = symbol
        self._name = name
        self._lang = lang
        if exchval is not None:
            self._exchval = exchval
        else:
            self._exchval = self._get_exchval(self._code)

    @property
    def code(self):
        """

        :return: The currency code.
        :rtype: str

        """
        return self._code

    @property
    def symbol(self):
        """

        :return: The currency symbol, or code if no symbol.
        :rtype: str

        """
        if self._symbol is not None:
            return self._symbol
        else:
            return self._code

    @property
    def name(self):
        if self._name is not None:
            return self._name
        else:
            return self._code

    @property
    def lang(self):
        return self._lang or 'en'

    @property
    def exchval(self):
        """
        :return: The exchange rate
        :rtype: float

        """
        return self._exchval

    @property
    def exch_rate(self):
        """
        The exchange rate in a human-friendly string.
        """
        return "{0}1/{1}{2:,.2f}".format(self.symbol, BASE_CURRENCY_SYMBOL, self.exchval)

    @staticmethod
    def _get_exchval(code):
        """
        Obtains the exchange rate of the currency definition's :attr:`code`
        using the `<http://fixer.io>`_ JSON API. The native currency is used
        as the reference.

        :param code: The currency code for which the exchange rate is needed.
        :type code: str
        :return: The exchange rate of currency specified by code vs the native
                 currency.
        :rtype: float

        """

        if BASE_CURRENCY == code:
            return 1
        if code == 'USD':
            return 72
        apiurl = 'http://data.fixer.io/api/latest?'
        params = {'access_key': FIXER_IO_API_KEY,
                  'symbols': ','.join([code, BASE_CURRENCY])}
        r = requests_session.get(apiurl, params=params)
        data = r.json()
        try:
            rate = float(data['rates'][BASE_CURRENCY]) / float(data['rates'][code])
        except KeyError:
            raise
        return rate

    def __eq__(self, other):
        """
        Two instances of :class:`CurrencyDefinition` will evaluate to be equal
        only when all three parameters of the instances are equal.
        """
        if self.code != other.code:
            return False
        if self.symbol != other.symbol:
            return False
        if self.exchval != other.exchval:
            return False
        return True

    def __repr__(self):
        return "<CurrencyDefinition {0} {1} {2}>" \
               "".format(self.code, self.symbol, self.exchval)


#: The native currency definition used by the module
#:
#: This definition uses the code contained in
#: :const:`tendril.config.BASE_CURRENCY` and symbol
#: :const:`tendril.config.BASE_CURRENCY_SYMBOL`. Application
#: code should import this definition instead of creating new currency
#: definitions whenever one is needed to represent a native currency value.
native_currency_defn = CurrencyDefinition(code=BASE_CURRENCY, 
                                          symbol=BASE_CURRENCY_SYMBOL,
                                          name=BASE_CURRENCY_NAME,
                                          lang=BASE_CURRENCY_LANG)


def _currency_parser(cv, value):
    # TODO Also manage currency definition?
    parts = value.split(' ')
    if len(parts) > 1:
        assert parts[0].strip() in [cv._currency_def.code,
                                    cv._currency_def.symbol]
        return Decimal(parts[1])
    else:
        return Decimal(parts[0])


class CurrencyValue(NumericalUnitBase):
    """
    Instances of this class define a specific currency value, or a certain
    sum of money.

    The `currency_def` can either be a :class:`CurrencyDefinition` instance
    (recommended), or a string containing the code for the currency.

    :param val: The numerical value.
    :param currency_def: The currency definition within which the value
                         is defined.
    :type currency_def: :class:`CurrencyDefinition` or str

    .. note:: Since the exchange rate is obtained at the instantiation of
              the :class:`CurrencyDefinition`, using a string instead of a
              predefined :class:`CurrencyDefinition` instance may result in
              instances of the same currency, but with different exchange
              rates.

    :ivar _currency_def: The currency definition of the source value of the
                         instance.
    :ivar _val: The numerical value in the source currency of the instance.

    .. rubric:: Arithmetic Operations

    .. autosummary::

        __add__
        __sub__
        __mul__
        __div__
        _cmpkey

    """

    _has_bare_order = True
    _orders = [('', 1)]
    _parse_func = _currency_parser

    def __init__(self, value, currency_def=native_currency_defn):
        if isinstance(currency_def, CurrencyDefinition):
            self._currency_def = currency_def
        else:
            self._currency_def = CurrencyDefinition(currency_def)
        super(CurrencyValue, self).__init__(value)

    @property
    def native_value(self):
        """
        The numerical value of the currency value in the native currency,
        i.e., that defined by :data:`native_currency_defn`.

        :rtype: float

        """
        return self._value * self._currency_def.exchval

    @property
    def native_string(self):
        """
        The string representation of the currency value in the native
        currency, i.e., that defined by :data:`native_currency_defn`.

        :rtype: str

        """
        return "{0} {1:,.2f}".format(BASE_CURRENCY_SYMBOL, self.native_value)
    
    @property
    def native_words(self):
        try:
            return num2words(self.native_value, to='currency', adjective=True,
                             currency=native_currency_defn.code,
                             lang=native_currency_defn.lang).title()
        except NotImplementedError:
            return "{0} {1}".format(
                native_currency_defn.name,
                num2words(self.native_value,
                          lang=native_currency_defn.lang).title()
            )

    @property
    def source_value(self):
        """
        The numerical value of the currency value in the source currency,
        i.e., that defined by :attr:`source_currency`.

        :rtype: float

        """
        return self._value

    @property
    def source_string(self):
        """
        The string representation of the currency value in the source
        currency, i.e., that defined by :attr:`source_currency`.

        :rtype: str

        """
        return "{0} {1:,.2f}".format(self._currency_def.symbol, self._val)
    
    @property
    def source_words(self):
        try:
            return num2words(self.source_value, to='currency', adjective=True,
                             currency=self._currency_def.code,
                             lang=self._currency_def.lang).title()
        except NotImplementedError:
            return "{0} {1}".format(
                self._currency_def.name,
                num2words(self.source_value,
                          lang=self._currency_def.lang).title()
            )

    @property
    def source_currency(self):
        """
        The currency definition of the source currency, i.e, the instance
        variable :data:`_currency_def`.

        :rtype: :class:`CurrencyDefinition`

        """
        return self._currency_def

    @property
    def exch_rate(self):
        """
        The applicable exchange rate in a human-friendly string.
        """
        return self._currency_def.exch_rate

    @property
    def is_foreign(self):
        """
        Whether the source currency is Foreign (``True``) or is the native
        currency (``False``).
        """
        if self._currency_def.code != BASE_CURRENCY:
            return True
        else:
            return False

    def __repr__(self):
        return self.native_string

    def __float__(self):
        return float(self.native_value)

    def __add__(self, other):
        """
        Addition of two :class:`CurrencyValue` instances returns a
        :class:`CurrencyValue` instance with the sum of the two operands,
        with currency conversion applied if necessary.

        If the :attr:`source_currency` of the two operands are equal,
        the result uses the the same :attr:`source_currency`. If not,
        the result is uses the :data:`native_currency_defn` as it's
        :attr:`source_currency`.

        If the other operand is a numerical type and evaluates to 0, this
        object is simply returned unchanged.

        Addition with all other Types / Classes is not supported.

        :rtype: :class:`CurrencyValue`
        """
        if isinstance(other, Number) and other == 0:
            return self
        if not isinstance(other, CurrencyValue):
            raise NotImplementedError
        if self._currency_def.symbol == other.source_currency.symbol:
            return CurrencyValue(
                self.source_value + other.source_value, self.source_currency
            )
        else:
            return CurrencyValue(
                self.native_value + other.native_value, native_currency_defn
            )

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __mul__(self, other):
        """
        Multiplication of one :class:`CurrencyValue` instance with a
        numerical type results in a :class:`CurrencyValue` instance,
        whose value is is the currency type operand's value multiplied
        by the numerical operand's value.

        The :attr:`source_currency` of the returned :class:`CurrencyValue`
        is the same as that of the currency type operand.

        Multiplication with all other Types / Classes is not supported.

        :rtype: :class:`CurrencyValue`
        """
        if isinstance(other, Number):
            return CurrencyValue(
                self.source_value * other, self.source_currency
            )
        elif isinstance(other, Percentage):
            return CurrencyValue(
                self.source_value * other.value / 100,
                self.source_currency
            )
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        """
        Division of one :class:`CurrencyValue` instance with a numerical type
        results in a :class:`CurrencyValue` instance, whose value is is the
        currency type operand's value divided by the numerical operand's
        value.

        The :attr:`source_currency` of the returned :class:`CurrencyValue`
        is the same as that of the currency type operand. In this case, the
        first operand must be a :class:`CurrencyValue`, and not the reverse.

        Division of one :class:`CurrencyValue` instance by another returns a
        numerical value, which is obtained by performing the division with the
        operands' :attr:`native_value`.

        Division with all other Types / Classes is not supported.

        :rtype: :class:`CurrencyValue`
        """
        if isinstance(other, Number):
            return CurrencyValue(
                self.source_value / other, self.source_currency
            )
        elif isinstance(other, CurrencyValue):
            return self.native_value / other.native_value
        else:
            raise NotImplementedError

    def __truediv__(self, other):
        return self.__div__(other)

    def __sub__(self, other):
        """
        Subtraction of two :class:`CurrencyValue` instances returns a
        :class:`CurrencyValue` instance with the difference of the two
        operands, with currency conversion applied if necessary.

        If :attr:`source_currency` of the two operands are equal,
        the result uses the the same :attr:`source_currency`. If not,
        the result is in the :data:`native_currency_defn`.

        If the other operand is a numerical type and evaluates to 0, this
        object is simply returned unchanged.

        Subtraction with all other Types / Classes is not supported.

        :rtype: :class:`CurrencyValue`
        """
        if isinstance(other, Number) and other == 0:
            return self
        elif not isinstance(other, CurrencyValue):
            raise NotImplementedError
        else:
            return self.__add__(other.__mul__(-1))

    def _cmpkey(self):
        """
        The comparison of two :class:`CurrencyValue` instances behaves
        identically to the comparison of the operands' :attr:`native_value`.

        Comparison with all other Types / Classes is not supported.
        """
        return self.native_value
