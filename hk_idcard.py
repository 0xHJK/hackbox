#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
    根据打码的身份证号码计算原始身份证号码
    usage: python3 hk_idcard.py <idcard number>
    example: python3 hk_idcard.py '1101012001****7770'
"""

import re
import sys
import time
import pprint


class IDCard:
    def __init__(self, idcard):
        if not idcard or len(idcard) != 18:
            print("身份证长度要求18位，不确定部分用*代替")
            return
        self.weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        self.check_code = "10X98765432"
        self.area = idcard[:6]
        self.year = idcard[6:10]
        self.mday = idcard[10:14]
        self.order = idcard[14:17]
        self.check = idcard[17]
        self.result_list = []

    def gen(self) -> list:
        """生成身份证号列表"""
        self.fix_area()
        self.fix_year()
        self.fix_mday()
        self.fix_order()
        idcard_list = [
            "%s%s%s%s" % (area, year, mday, order)
            for area in self.area_list
            for year in self.year_list
            for mday in self.mday_list
            for order in self.order_list
        ]
        for idcard in idcard_list:
            total = sum([x[0] * int(x[1]) for x in zip(self.weight, list(idcard))])
            check = self.check_code[total % 11]
            if self.check != "*" and self.check != check:
                continue
            self.result_list.append("%s%s" % (idcard, check))
        return self.result_list

    def fix_area(self):
        # 暂不处理区号
        self.area_list = [self.area]

    def fix_year(self):
        if not "*" in self.year:
            self.year_list = [self.year]
            return
        self.year_list = []
        rex = self.year.replace("*", "\d")
        for i in range(1900, 2020):
            s = str(i)
            if re.match(rex, s):
                self.year_list.append(s)

    def fix_mday(self):
        if not "*" in self.mday:
            self.mday_list = [self.mday]
            return
        self.mday_list = []
        rex = self.mday.replace("*", "\d")
        bgn = int(time.mktime(time.strptime("20000101", "%Y%m%d")))
        end = int(time.mktime(time.strptime("20001231", "%Y%m%d")))
        mday_list = [
            time.strftime("%Y%m%d", time.localtime(i))[4:]
            for i in range(bgn, end + 1, 3600 * 24)
        ]
        for mday in mday_list:
            if re.match(rex, mday):
                self.mday_list.append(mday)

    def fix_order(self):
        # 暂不处理序列号
        self.order_list = [self.order]


if __name__ == "__main__":
    if not sys.argv or len(sys.argv[1]) != 18:
        print("usage: python3 hk_idcard.py '1101012001****7770'")
        exit(-1)
    idcard = IDCard(sys.argv[1])
    result_list = idcard.gen()
    pprint.pprint(result_list)
    print("Length: ", len(result_list))
