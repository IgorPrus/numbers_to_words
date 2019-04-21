# -*- coding: utf-8 -*-
# Copyright (c) 2019, IgorPrus.  All Rights Reserved.

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ('нуль',)

ONES_FEMININE = {
    1: ('адна',),
    2: ('дзве',),
    3: ('тры',),
    4: ('чатыры',),
    5: ('пяць',),
    6: ('шэсць',),
    7: ('сем',),
    8: ('восем',),
    9: ('дзевяць',),
}

ONES = {
    1: ('адзін',),
    2: ('два',),
    3: ('тры',),
    4: ('чатыры',),
    5: ('пяць',),
    6: ('шэсць',),
    7: ('сем',),
    8: ('восем',),
    9: ('дзевяць',),
}

TENS = {
    0: ('дзесяць',),
    1: ('адзінаццаць',),
    2: ('дванаццаць',),
    3: ('трынаццаць',),
    4: ('чатырнаццаць',),
    5: ('пятнаццаць',),
    6: ('шаснаццаць',),
    7: ('семнаццаць',),
    8: ('васемнаццаць',),
    9: ('дзевятнаццаць',),
}

TWENTIES = {
    2: ('дваццаць',),
    3: ('трыццаць',),
    4: ('сорак',),
    5: ('пяцьдзесят',),
    6: ('шэсцьдзесят',),
    7: ('семдзесят',),
    8: ('восемдзесят',),
    9: ('дзевяноста',),
}

HUNDREDS = {
    1: ('сто',),
    2: ('дзвесце',),
    3: ('трыста',),
    4: ('чатырыста',),
    5: ('пяцьсот',),
    6: ('шэсцьсот',),
    7: ('семсот',),
    8: ('восемсот',),
    9: ('дзевяцьсот',),
}

THOUSANDS = {
    1: ('тысяча', 'тысячы', 'тысяч'),  # 10^3
    2: ('мільён', 'мільёна', 'мільёнаў'),  # 10^6
    3: ('мільярд', 'мільярда', 'мільярдаў'),  # 10^9
    4: ('трыльён', 'трыльёна', 'трыльёнаў'),  # 10^12
    5: ('квадрыльён', 'квадрыльёна', 'квадрыльёнаў'),  # 10^15
    6: ('квінтыльён', 'квінтыльёна', 'квінтыльёнаў'),  # 10^18
    7: ('секстыльён', 'секстыльёна', 'секстыльёнаў'),  # 10^21
    8: ('септільён', 'септільёна', 'септільёнаў'),  # 10^24
    9: ('октільён', 'октільёна', 'октільёнаў'),  # 10^27
    10: ('нонільён', 'нонільёна', 'нонільёнаў'),  # 10^30
}


class Num2Word_BY(Num2Word_Base):
    CURRENCY_FORMS = {
        'RUB': (
            ('рубель', 'рубля', 'рублёў'), ('капейка', 'капейкі', 'капеек')
        ),
        'EUR': (
            ('еўра', 'еўра', 'еўра'), ('цэнт', 'цэнта', 'цэнтаў')
        ),
        'USD': (
            ('даляр', 'даляра', 'даляраў'), ('цэнт', 'цэнта', 'цэнтаў')
        ),
    }

    def setup(self):
        self.negword = "мінус"
        self.pointword = "коска"
        self.ords = {"нуль": "нулявы",
                     "адзін": "першы",
                     "два": "другі",
                     "тры": "трэці",
                     "чатыры": "чацвёрты",
                     "пяць": "пяты",
                     "шэсць": "шосты",
                     "сем": "сёмы",
                     "восем": "восьмай",
                     "дзевяць": "дзявяты",
                     "сто": "соты"}
        self.ords_feminine = {"адзін": "",
                              "адна": "",
							  "дзве": "двух",
                              "тры": "трох",
                              "чатыры": "чатырох",
                              "пяць": "пяці",
                              "шэсць": "шасці",
                              "сем": "сямі",
                              "восем": "васьмі",
                              "дзевяць": "дзевяці"}

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            return u'%s %s %s' % (
                self._int2word(int(left)),
                self.pointword,
                self._int2word(int(right))
            )
        else:
            return self._int2word(int(n))

    def pluralize(self, n, forms):
        if n % 100 < 10 or n % 100 > 20:
            if n % 10 == 1:
                form = 0
            elif 5 > n % 10 > 1:
                form = 1
            else:
                form = 2
        else:
            form = 2
        return forms[form]

    def to_ordinal(self, number):
        self.verify_ordinal(number)
        outwords = self.to_cardinal(number).split(" ")
        lastword = outwords[-1].lower()
        try:
            if len(outwords) > 1:
                if outwords[-2] in self.ords_feminine:
                    outwords[-2] = self.ords_feminine.get(
                        outwords[-2], outwords[-2])
                elif outwords[-2] == 'дзесяць':
                    outwords[-2] = outwords[-2][:-1] + 'i'
            if len(outwords) == 3:
                if outwords[-3] in ['адзін', 'адна']:
                    outwords[-3] = ''
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[:-3] in self.ords_feminine:
                lastword = self.ords_feminine.get(
                    lastword[:-3], lastword) + "соты"
            elif lastword[-1] == "ь" or lastword[-2] == "т":
                lastword = lastword[:-1] + "ый"
            elif lastword[-1] == "к":
                lastword = lastword.replace('орак', 'аракавы') #+ "овой"
            elif lastword[-7:] == "мдзесят":
                lastword = lastword.replace('емдзесят', 'ямідзесяты')
            elif lastword[-6:] == "дзесят":
                lastword = lastword.replace('ь', 'и') + 'ый'
            elif lastword[-2] == "ч" or lastword[-1] == "ч":
                if lastword[-2] == "ч":
                    lastword = lastword[:-1] + "ный"
                if lastword[-1] == "ч":
                    lastword = lastword + "ный"
            elif lastword[-1] == "н" or lastword[-2] == "н":
                lastword = lastword[:lastword.rfind('н') + 1] + "ный"
            elif lastword[-1] == "д" or lastword[-2] == "д":
                lastword = lastword[:lastword.rfind('д') + 1] + "ный"
        outwords[-1] = self.title(lastword)
        return " ".join(outwords).strip()

    def _cents_verbose(self, number, currency):
        return self._int2word(number, currency == 'RUB')

    def _int2word(self, n, feminine=False):
        if n < 0:
            return ' '.join([self.negword, self._int2word(abs(n))])

        if n == 0:
            return ZERO[0]

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0:
                ones = ONES_FEMININE if i == 1 or feminine and i == 0 else ONES
                words.append(ones[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return ' '.join(words)
