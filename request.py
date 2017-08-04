#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: stskyblade
@contact: stskyblade@outlook.com
@file: request.py
@time: 7/31/2017 7:22 PM
"""

from urllib.parse import unquote
import re
import os


class Request(object):
    """docstring for Request"""
    def __init__(self, rqstB):
        self.rqst = rqstB.decode('utf8')
        self._Dict = {}
        self._makeDict()

    def _makeDict(self):
        tmp = self.rqst.split('\r\n')
        firstLine = tmp[0]
        headers = tmp[1:]

        print("firstLine:", firstLine)
        self._Dict['REQUEST_METHOD'], self._Dict['PATH_INFO'],\
            self._Dict['SERVER_PROTOCOL'] = firstLine.split(' ')
        self._Dict['PATH_INFO'] = unquote(self._Dict['PATH_INFO'])

        path = self._Dict['PATH_INFO']
        if '?' in path:
            # handle query string
            whatLoc = path.index('?')
            self._Dict['PATH_INFO'] = path[:whatLoc]
            query_string = path[whatLoc + 1:]
            self._Dict['QUERY_STRING'] = query_string

            args = query_string.split('&')
            self._Dict['GET'] = {}
            for arg in args:
                k, v = arg.split('=')
                self._Dict['GET'][k] = v

        for header in headers:
            if header:
                k, v = header.split(':', 1)
                self._Dict['HTTP_' + k.upper().replace('-', "_")] = v

    def handle_post(self, contentB):
        content_type = self._Dict['HTTP_CONTENT_TYPE']
        if 'multipart' in content_type:
            self._handle_post(contentB,
                              True,
                              content_type[content_type.index('=') + 1:].encode('utf8'))
        else:
            self._handle_post(contentB)

    def _handle_post(self, rqstBodyB, multi=False, boundaryB=None):
        if multi:
            parts = rqstBodyB.split(boundaryB)[1:-1]
            self._Dict['POST'] = {}
            for part in parts:
                self._handle_part(part)
        else:
            from urllib.parse import unquote

            rqstBody = unquote(rqstBodyB.decode('utf8'))
            print(rqstBody)
            args = rqstBody.split('&')
            self._Dict['POST'] = {}
            for arg in args:
                k, v = arg.split('=')
                self._Dict['POST'][k] = v

    def _handle_part(self, partB):
        if b'filename=' not in partB:
            k = re.findall(b'".*"', partB)[0].strip(b'"')
            v = re.findall(b'\r\n\r\n.*\r\n', partB)[0].strip(b'\r\n')
            self._Dict['POST'][k.decode('utf8')] = v.decode('utf8')
        else:
            k, filename = re.findall(b'name="[\w\.]*"', partB)
            k = k.strip(b'name=').strip(b'"').decode('utf8')
            filename = filename.strip(b'name=').strip(b'"').decode('utf8')
            data = partB.split(b'\r\n\r\n')[1].strip(b'\r\n--')

            # write file
            if not os.path.isdir('static/tmp'):
                os.mkdir('static/tmp')
            filename = 'static/tmp/' + filename
            with open(filename, 'wb') as f:
                f.write(data)
                f.close()

            self._Dict['POST'][k] = filename

    def __str__(self):
        return str(self._Dict)

    def dict(self):
        return self._Dict


def main():
    rqst = (b'GET / HTTP/1.1\r\n'
            b'Host: 127.0.0.1:5000\r\n'
            b'Connection: keep-alive\r\n'
            b'Cache-Control: max-age=0\r\n'
            b'Upgrade-Insecure-Requests: 1\r\n'
            b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            b'AppleWebKit/537.36 (KHTML, like Gecko) '
            b'Chrome/59.0.3071.115 Safari/537.36\r\n'
            b'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,'
            b'image/webp,image/apng,*/*;q=0.8\r\nDNT: 1\r\n'
            b'Accept-Encoding: gzip, deflate, br\r\n'
            b'Accept-Language: en-US,en;q=0.8\r\n\r\n')
    print(type(rqst))
    r = Request(rqst)
    print(r)


if __name__ == '__main__':
    main()
