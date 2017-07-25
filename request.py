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


class Request(object):
        """docstring for Request"""
        def __init__(self, rqstB):
                self.rqstB = rqstB
                self.rqst = rqstB.decode('utf8')

        def __str__(self):
                return self.rqst

r = Request(rqst)
print(r)
