#!/usr/bin/env python3
# -*- coding=utf-8 -*-

"""
    骚扰电话识别，从多个搜索引擎搜索电话号码信息
    usage: python3 hk_idcard.py <phone number>
    example: python3 hk_idcard.py 18811223344
"""

import re
import sys
import click
import requests
from pyquery import PyQuery as pq


def echo(msg):
    fg = "yellow" if "标记" in msg else "green"
    fg = "red" if "骚扰" in msg else fg
    click.secho(msg, fg=fg)


def query_baidu(session, num):
    click.echo("From baidu.com:")
    r = session.get(
        "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%s" % num
    )
    d = pq(r.text)
    result = " ".join(d(".c-border .c-row").text().split())
    echo("[%s] %s" % (r.status_code, result))


def query_360(session, num):
    click.echo("From so.com:")
    r = session.get("https://www.so.com/s?ie=utf-8&shb=1&src=home_so.com&q=%s" % num)
    d = pq(r.text)
    result = " ".join(d(".mohe-wrap").text().split())
    echo("[%s] %s" % (r.status_code, result))


def query_sogou(session, num):
    click.echo("From sogou.com:")
    session.headers.update({"referer": "https://www.sogou.com"})
    r = session.get("https://www.sogou.com/web?ie=UTF-8&query=%s" % num)
    num = num.replace("-", "")
    rex = "[\"']%s[\"']\,.+\);" % num
    result = []
    for word in re.findall(rex, r.text):
        word = re.sub("'|\"|\)|\;", "", word)
        t_list = [x.strip() for x in word.split(",") if len(x) > 2]
        word = " ".join(list(set(t_list)))
        result.append(word)
    result = " ".join(result)
    echo("[%s] %s" % (r.status_code, result))


@click.command()
@click.argument("num")
def main(num):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "referer": "https://www.baidu.com",
        }
    )
    try:
        query_baidu(session, num)
    except:
        pass
    try:
        query_360(session, num)
    except:
        pass
    try:
        query_sogou(session, num)
    except:
        pass


if __name__ == "__main__":
    main()
