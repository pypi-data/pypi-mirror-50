#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
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

