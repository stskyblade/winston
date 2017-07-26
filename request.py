def strToByte(s):
    return s.encode('utf8')


def byteToStr(b):
    return b.decode('utf8')


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

        self._Dict['METHOD'], self._Dict['URL'], self._Dict['HTTP-VERSION'] \
            = firstLine.split(' ')
        for header in headers:
            if header:
                k, v = header.split(':', 1)
                self._Dict[k.upper()] = v

    def __str__(self):
        return str(self._Dict)


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


# {'ACCEPT-LANGUAGE': ' en-US,en;q=0.8', 'URL': '/', 'METHOD': 'GET', 'HTTP-VERSION': 'HTTP/1.1', 'ACCEPT': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'USER-AGENT': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36', 'HOST': ' 127.0.0.1:5000', 'CONNECTION': ' keep-alive', 'ACCEPT-ENCODING': ' gzip, deflate, br', 'DNT': ' 1', 'CACHE-CONTROL': ' max-age=0', 'UPGRADE-INSECURE-REQUESTS': ' 1'}

if __name__ == '__main__':
    main()
