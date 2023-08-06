#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
import math
class number2str_th:

    def __init__(self, number, currency):
        self.number = number
        self.currency = currency

    def num_to_text_th(self):
        number = '%.2f' % float(self.number)
        units_name = self.currency
        list = str(number).split('.')
        start_word = self.control(list[0])
        end_word = self.control(list[1])
        cents_number = int(list[1])
        if cents_number == 0:
            cents_name = 'ถ้วน'
        else:
            cents_name = (cents_number > 1) and 'สตางค์' or 'สตางค์'
        final_result = start_word + units_name + end_word + cents_name
        # _logger.debug('amount to text th >>>>>>>>> %r',final_result)
        # print "test"
        # print final_result
        return final_result
    #
    def control(self, val):
        lek = ("ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า")
        luk = ("สิบ", "ร้อย", "พัน", "หมื่น", "แสน", "ล้าน")
        text = ''

        def thainumtext(val):
            i = 0
            n, l = len(val), len(val)
            text = ''
            temp_int = 0
            while n > 0:
                temp_int = int(val[i])
                if (temp_int > 0):
                    if ((n == 1) and temp_int == 1 and l > 1):
                        text = text + 'เอ็ด'
                    elif ((2 == n) and temp_int == 1):
                        pass
                    elif ((2 == n) and temp_int == 2):
                        text = text + 'ยี่'
                    else:
                        text = text + lek[temp_int]
                    if n > 1:
                        text = text + luk[n - 2]
                n = n - 1
                i += 1
            return text

        n = len(val)
        if n == 1: return lek[int(val)]
        nlist = []
        n = 6
        temp = ''
        for i in reversed(val):
            temp = i + temp
            n = n - 1
            if n == 0:
                nlist.append(temp)
                temp = ''
                n = 6
        else:
            if temp <> '':  nlist.append(temp)
        n = 1
        for i in (nlist):
            if n:
                text = thainumtext(i) + text
                n = 0
            else:
                text = thainumtext(i) + 'ล้าน' + text
        return text


class munber2str_en:

    def __init__(self, number, currency):
        self.number = number
        self.currency = currency

    def num_to_en_text(self):
        #         numbers = [1.37, 0.07, 123456.00, 987654.33]
        number = '%.2f' % float(self.number)
        numbers = [number]
        unit_before = ''
        unit_after = ''
        dollars = ''
        cents = ''
        result = ''
        if self.currency == 'THB':
            unit_before = 'Baht'
            unit_after = 'Stang'
        elif self.currency == 'USD':
            unit_before = 'Dollar'
            unit_after = 'Cent'
        #         else:
        #             unit_before = ''
        #             unit_after = ''

        if unit_before == '':
            for number in numbers:
                dollars, cents = [(num) for num in str(number).split(".")]
                tmp_cent = cents
                if int(cents[0]) == 0:
                    cents = int(cents)

                    dollars = self.num2eng(dollars)
                    if dollars.strip() == "one":
                        dollars = dollars + unit_before + " and "
                    else:
                        dollars = dollars + unit_before + " and "
                    cents = self.num2eng(cents) + unit_after
                    if int(tmp_cent) != 0:
                        cents = 'Zero ' + cents

                elif int(cents[0]) != 0:
                    cents = int(cents) * 10
                    dollars = self.num2eng(dollars)
                    if dollars.strip() == "one":
                        dollars = dollars + unit_before + " and "
                    else:
                        dollars = dollars + unit_before + " and "

                    cents = self.num2eng(cents) + unit_after

            result = dollars + cents + "(" + self.currency + ")"

        else:
            for number in numbers:
                dollars, cents = [(num) for num in str(number).split(".")]
                tmp_cent = cents
                if int(cents[0]) == 0:
                    cents = int(cents)
                    dollars = self.num2eng(dollars)
                    if dollars.strip() == "one":
                        dollars = dollars + unit_before + " and "
                    else:
                        dollars = dollars + unit_before + " and "

                    cents = self.num2eng(cents) + unit_after
                    if int(tmp_cent) != 0:
                        cents = 'Zero ' + cents

                elif int(cents[0]) != 0:
                    cents = int(cents) * 10
                    dollars = self.num2eng(dollars)
                    if dollars.strip() == "one":
                        dollars = dollars + unit_before + " and "
                    else:
                        dollars = dollars + unit_before + " and "

                    cents = self.num2eng(cents) + unit_after
            #                 if cents > 0 or cents < 9:
            #                     cents = cents*10
            #                 dollars = self.num2eng(dollars)
            #                 if dollars.strip() == "one":
            #                     dollars = dollars + unit_before +" and "
            #                 else:
            #                     dollars = dollars + unit_before +" and "
            #
            #                 cents = self.num2eng(cents) + unit_after
            result = dollars + cents

        return result

    _PRONOUNCE = [
        'Vigintillion',
        'Novemdecillion',
        'Octodecillion',
        'Septendecillion',
        'Sexdecillion',
        'Quindecillion',
        'Quattuordecillion',
        'Tredecillion',
        'Duodecillion',
        'Undecillion',
        'Decillion',
        'Nonillion',
        'Octillion',
        'Septillion',
        'Sextillion',
        'Quintillion',
        'Quadrillion',
        'Trillion',
        'Billion',
        'Million',
        'Thousand',
        ''
    ]

    _SMALL = {
        '0': '',
        '1': 'One',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine',
        '10': 'Ten',
        '11': 'Eleven',
        '12': 'Twelve',
        '13': 'Thirteen',
        '14': 'Fourteen',
        '15': 'Fifteen',
        '16': 'Sixteen',
        '17': 'Seventeen',
        '18': 'Eighteen',
        '19': 'Nineteen',
        '20': 'Twenty',
        '30': 'Thirty',
        '40': 'Forty',
        '50': 'Fifty',
        '60': 'Sixty',
        '70': 'Seventy',
        '80': 'Eighty',
        '90': 'Ninety'
    }
    def get_num(self, num):
        return self._SMALL.get(num, '')

    def triplets(self, l):
        '''Split list to triplets. Pad last one with '' if needed'''
        res = []
        for i in range(int(math.ceil(len(l) / 3.0))):
            sect = l[i * 3: (i + 1) * 3]
            if len(sect) < 3:  # Pad last section
                sect += [''] * (3 - len(sect))
            res.append(sect)
        return res

    def norm_num(self, num):
        """Normelize number (remove 0's prefix). Return number and string"""
        n = int(num)
        return n, str(n)

    def small2eng(self, num):
        '''English representation of a number <= 999'''
        n, num = self.norm_num(num)
        hundred = ''
        ten = ''
        if len(num) == 3 and num > 0:  # Got hundreds
            hundred = self.get_num(num[0]) + ' hundred'
            num = num[1:]
            n, num = self.norm_num(num)
        if (n > 20) and (n != (n / 10 * 10)):  # Got ones
            tens = self.get_num(num[0] + '0')
            ones = self.get_num(num[1])
            ten = tens + ' ' + ones
        else:
            ten = self.get_num(num)
        if hundred and ten:
            return hundred + ' ' + ten
            # return hundred + ' and ' + ten
        else:  # One of the below is empty
            return hundred + ten

    def num2eng(self, num):
        '''English representation of a number'''
        num = str(long(num))  # Convert to string, throw if bad number
        if (len(num) / 3 >= len(self._PRONOUNCE)):  # Sanity check
            raise ValueError('Number too big')

        if num == '0':  # Zero is a special case
            return 'Zero '

        # Create reversed list
        x = list(num)
        x.reverse()
        pron = []  # Result accumolator
        ct = len(self._PRONOUNCE) - 1  # Current index
        for a, b, c in self.triplets(x):  # Work on triplets
            p = self.small2eng(c + b + a)
            if p:
                pron.append(p + ' ' + self._PRONOUNCE[ct])
            ct -= 1
        # Create result
        pron.reverse()
        return ', '.join(pron)

