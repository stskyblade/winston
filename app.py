#!/usr/bin/env python
# encoding: utf-8

"""
@version: v0.1
@author: stskyblade
@contact: stskyblade@outlook.com
@file: app.py
@time: 7/31/2017 7:59 PM
"""


class Winston(object):
    def __init__(self):
        self.url_routes = {}
        self.add_url_route('no_route', no_route)

    def add_url_route(self, url, func):
        if '<' in url:
            self.url_routes['endpoint:' + url[:url.index('<')-1]] = func
        else:
            self.url_routes[url] = func

    def route(self, url):
        """

        :rtype: bytes
        """
        print('request URL: %s' % url)
        func = self.url_routes.get(url, None)
        if (not func) and url[-4] != '.':
            # match url, '/hello', '/hello/ngp'
            endpoint = 'endpoint:' + url[:url.rfind('/')]
            parm = url[url.rfind('/')+1:]
            print('call endpoint %s(%s)...' % (str(endpoint), parm))
            return self.url_routes.get(endpoint, None)(parm).encode('utf8')
        elif func:
            print('call func %s()...' % str(func))
            print(func())
            return func().encode('utf8')
        else:
            return self.url_routes.get('no_route', None)().encode('utf8')

    def wsgi_app(self, env, start_response):
        # analyze env
        response_body = self.route(env['PATH_INFO'])

        status = "200 OK"
        length = str(len(response_body))
        response_headers = [
            ('Content-Length', length)
        ]

        start_response(status, response_headers)
        print(response_body)
        return [response_body]

    def run(self, port, once=True):
        import socket
        from request import Request

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        server_sock.listen(5)

        try:
            while True:
                # receive request
                print('waiting connection...')
                client_sock, addr = server_sock.accept()
                print('connected from: <%s:%s>' % addr)
                rqst = Request(client_sock.recv(1024)).dict()

                def start_response(status, response_headers):
                    resp = 'HTTP/1.1 %s\r\n' % status
                    headers = ['%s:%s' % (name, value) for (name, value) in response_headers]
                    response_header = (resp + '\r\n'.join(headers) + '\r\n\r\n').encode('utf8')

                    # print(type(response_header), response_header)
                    client_sock.send(response_header)

                bodys = self.wsgi_app(rqst, start_response)
                for body in bodys:
                    # print(type(body),body)
                    client_sock.send(body)

                client_sock.close()
                if once:
                    server_sock.close()
                    exit()
        except KeyboardInterrupt:
            if client_sock:
                client_sock.close()
            server_sock.close()
            if once:
                exit()


def no_route():
    return 'no route yet'
