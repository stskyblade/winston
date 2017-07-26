class Response(object):
    """docstring for Response"""
    def __init__(self, conn):
        self.conn = conn
        self.headers = {}

    def set_headers(self, headers):
        # [(name1, value1), (n2, v2)]
        for header in headers:
            k, v = header
            self.headers[k] = v

    def _make_response(self, status, body):
        # body = body.encode('utf8')

        headers = 'HTTP/1.1 %s\r\n' % status
        for (k, v) in self.headers.items():
            headers += '%s:%s\r\n' % (k, v)
        headers += '\r\n%s' % body
        return headers.encode('utf8')

    def start_response(self, status, body):
        # start_response('200 OK','Hello,world',)
        self.set_headers([('Content-Length', len(body.encode('utf8')))])
        print('construct response...')
        resp = self._make_response(status, body)
        print(resp)
        print('send response...')
        self.conn.send(resp)
