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
    def __init__(self, debug=False):
        self.url_routes = {}
        if debug:
            self.DEBUG = True

        self.add_url_route('not_found', not_found)
        self.add_url_route('/static/<file>', static)
        self.add_url_route('/form_print', form_print)

    def add_url_route(self, url, func):
        '''
        1,/hello->['/hello']
        2,/hello/<name>->['P:/hello']
        '''
        if '<' in url:
            self.url_routes['P:' + url[:url.index('<') - 1]] = func
        else:
            self.url_routes[url] = func

    def route(self, url):
        """
        return route function
        :url:   string
        :rtype: (parmFlag, func)
        """

        func = self.url_routes.get(url, None)

        if url == '/favicon.ico':
            return (1, self.url_routes.get('not_found', None))
        elif not func:
            # match url, '/hello/<name>'
            endpoint = 'P:' + url[:url.rfind('/')]
            return (0, self.url_routes.get(endpoint, None))
        elif func:
            # match url, '/hello'
            return (1, func)
        else:
            # 404 NOT FOUND
            return (1, self.url_routes.get('not_found', None))

    def wsgi_app(self, env, start_response):
        # analyze env
        url = env['PATH_INFO']
        self.logging(url, msg='URL')
        parmFlag, func = self.route(url)

        # generate response_body
        if '/static/' in url:
            response_body = self.route('P:/static')[1](url[7:])
        elif '/env' in url:
            envs = ['%s:%s' % (k, v) for (k, v) in env.items()]
            response_body = '\n'.join(envs).encode('utf8')
        elif url == '/form_print':
            response_body = func(env).encode('utf8')
        elif parmFlag:
            response_body = func().encode('utf8')
        else:
            parm = url[url.rfind('/') + 1:]
            response_body = func(parm).encode('utf8')

        status = "200 OK"
        length = str(len(response_body))
        response_headers = [
            ('Content-Length', length)
        ]

        start_response(status, response_headers)
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
                data = client_sock.recv(1024)
                print('\n')
                self.logging(data.decode('utf8'), 'request data')
                rqst = Request(data)

                # handle request body
                length = rqst.dict().get('HTTP_CONTENT_LENGTH', None)
                if length:
                    content_type = rqst.dict()['HTTP_CONTENT_TYPE']
                    if 'multipart' in content_type:
                        body = client_sock.recv(int(length))
                        self.logging(body, 'request content')
                        rqst.handle_post(body, True, content_type[content_type.index('=') + 1:].encode('utf8'))
                    else:
                        body = client_sock.recv(int(length))
                        self.logging(body, 'request content')
                        rqst.handle_post(body)

                def start_response(status, response_headers):
                    resp = 'HTTP/1.1 %s\r\n' % status
                    headers = ['%s:%s' % (name, value)
                               for (name, value) in response_headers]
                    response_header = resp + '\r\n'.join(headers) + '\r\n\r\n'
                    response_header = response_header.encode('utf8')

                    # print(type(response_header), response_header)
                    client_sock.send(response_header)

                bodys = self.wsgi_app(rqst.dict(), start_response)
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

    def logging(self, var, msg=None):
        if self.DEBUG:
            if msg:
                print('LOG: %s\nLOG VAR: %s' % (msg, var))
            else:
                print('LOG VAR: %s' % (var))


def not_found():
    return '<h1>404 NOT FOUND</h1>'


def static(path):
    file = 'static/' + path
    with open(file, 'rb') as fopen:
        data = fopen.read()
        fopen.close()
    return data


def form_print(env):
    return str(env['POST'] or env['GET'])
