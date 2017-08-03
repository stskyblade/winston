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


def main(inside_server=True):
    w = Winston(debug=True)

    def hello():
        return '<h1>hello,world</h1>'

    def hel(name):
        return '<h1>hello,%s</h1>' % name

    w.add_url_route('/hello', hello)
    w.add_url_route('/hello/<name>', hel)

    if inside_server:
        w.run(5000, once=False)
    else:
        from wsgiref.simple_server import make_server

        httpd = make_server('127.0.0.1', 5000, w.wsgi_app)
        print('Serving on port 5000...')
        httpd.serve_forever()


if __name__ == '__main__':
    main(1)
