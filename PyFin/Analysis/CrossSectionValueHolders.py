# -*- coding: utf-8 -*-
u"""
Created on 2017-1-6

@author: cheng.li
"""

import copy
from PyFin.Analysis.SecurityValueHolders import SecuritiesValues
from PyFin.Analysis.SecurityValueHolders import SecurityValueHolder


class CrossSectionValueHolder(SecurityValueHolder):

    def __init__(self, innerValue):
        if isinstance(innerValue, SecurityValueHolder):
            self._inner = copy.deepcopy(innerValue)
        else:
            # TODO: make the rank value holder workable for a symbol
            raise ValueError("Currently only value holder input is allowed for rank holder.")
        self._window = self._inner.window
        self._returnSize = self._inner.valueSize
        self._dependency = copy.deepcopy(self._inner._dependency)
        self.updated = False
        self.cached = SecuritiesValues()

    @property
    def symbolList(self):
        return self._inner.symbolList

    @property
    def holders(self):
        return self._inner.holders

    def push(self, data):
        self._inner.push(data)
        self.updated = False


class CSRankedSecurityValueHolder(CrossSectionValueHolder):

    def __init__(self, innerValue):
        super(CSRankedSecurityValueHolder, self).__init__(innerValue)

    @property
    def value(self):
        if self.updated:
            return self.cached
        else:
            raw_values = self._inner.value
            self.cached = raw_values.rank(ascending=False)
            self.updated = True
            return self.cached

    def value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            raw_values = self._inner.value
            self.cached = raw_values.rank(ascending=False)
            self.updated = True
            return self.cached[name]

    def value_by_names(self, names):
        raw_values = self._inner.value_by_names(names)
        raw_values = raw_values.rank(ascending=False)
        return raw_values


class CSAverageSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue):
        super(CSAverageSecurityValueHolder, self).__init__(innerValue)

    @property
    def value(self):
        if self.updated:
            return self.cached
        else:
            raw_values = self._inner.value
            mean_value = raw_values.mean()
            self.cached = SecuritiesValues(mean_value, raw_values.index)
            self.updated = True
            return self.cached

    def value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            raw_values = self._inner.value
            mean_value = raw_values.mean()
            self.cached = SecuritiesValues(mean_value, raw_values.index)
            self.updated = True
            return self.cached[name]

    def value_by_names(self, names):
        raw_values = self._inner.value_by_names(names)
        mean_value = raw_values.mean()
        raw_values = SecuritiesValues(mean_value, raw_values.index)
        return raw_values[names]


class CSAverageAdjustedSecurityValueHolder(CrossSectionValueHolder):
    def __init__(self, innerValue):
        super(CSAverageAdjustedSecurityValueHolder, self).__init__(innerValue)

    @property
    def value(self):
        if self.updated:
            return self.cached
        else:
            raw_values = self._inner.value
            self.cached = raw_values - raw_values.mean()
            self.updated = True
            return self.cached

    def value_by_name(self, name):
        if self.updated:
            return self.cached[name]
        else:
            raw_values = self._inner.value
            self.cached = raw_values - raw_values.mean()
            self.updated = True
            return self.cached[name]

    def value_by_names(self, names):
        raw_values = self._inner.value_by_names(names)
        raw_values = raw_values - raw_values.mean()
        return raw_values[names]