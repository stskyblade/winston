class Winston(object):
    def __init__(self):
        pass

    def wsgi_app(self, env, start_response):
        # return env
        response_body_list = ["%s : %s" % (k, v) for k, v in sorted(env.items())]
        response_body = "\n".join(response_body_list).encode('utf8')

        status = "200 OK"
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response_body)))
        ]

        start_response(status, response_headers)
        return [response_body]

    def run(self, port):
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
        except Exception:
            if client_sock:
                client_sock.close()
            server_sock.close()


def main():
    from wsgiref.simple_server import make_server

    w = Winston()
    httpd = make_server('127.0.0.1', 5000, w.wsgi_app)
    httpd.handle_request()

    print('end')

if __name__ == '__main__':
    main()
