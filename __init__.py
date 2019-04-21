# -*- coding: utf-8 -*-
# Copyright (c) 2019, IgorPrus.  All Rights Reserved.

from __future__ import unicode_literals

from . import (lang_BY, lang_EN, lang_RU)

CONVERTER_CLASSES = {
	'by': lang_BY.Num2Word_BY(),
    'en': lang_EN.Num2Word_EN(),
    'ru': lang_RU.Num2Word_RU(),
}


CONVERTES_TYPES = ['cardinal', 'ordinal', 'ordinal_num', 'year', 'currency']


def num2words(number, ordinal=False, lang='en', to='cardinal', **kwargs):
    # We try the full language first
    if lang not in CONVERTER_CLASSES:
        # ... and then try only the first 2 letters
        lang = lang[:2]
    if lang not in CONVERTER_CLASSES:
        raise NotImplementedError()
    converter = CONVERTER_CLASSES[lang]
    if isinstance(number, str):
        number = converter.str_to_number(number)
    # backwards compatible
    if ordinal:
        return converter.to_ordinal(number)

    if to not in CONVERTES_TYPES:
        raise NotImplementedError()

    return getattr(converter, 'to_{}'.format(to))(number, **kwargs)
