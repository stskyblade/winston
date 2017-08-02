#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: stskyblade
@contact: stskyblade@outlook.com
@file: test.py
@time: 7/31/2017 7:22 PM
"""

from app import Winston


def main():
    w = Winston()

    def hello():
        return '<h1>hello,world</h1>'

    def hel(name):
        return '<h1>hello,%s</h1>' % name

    w.add_url_route('/hello', hello)
    w.add_url_route('/hello/<name>', hel)
    w.run(5000, once=False)
    print('end')

if __name__ == '__main__':
    main()
