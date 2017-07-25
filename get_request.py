# rqst = (b'GET / HTTP/1.1\r\n'
#         'Host: 127.0.0.1:5000\r\n'
#         'Connection: keep-alive\r\n'
#         'Cache-Control: max-age=0\r\n'
#         'Upgrade-Insecure-Requests: 1\r\n'
#         'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#         'AppleWebKit/537.36 (KHTML, like Gecko) '
#         'Chrome/59.0.3071.115 Safari/537.36\r\n'
#         'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,'
#         'image/webp,image/apng,*/*;q=0.8\r\nDNT: 1\r\n'
#         'Accept-Encoding: gzip, deflate, br\r\n'
#         'Accept-Language: en-US,en;q=0.8\r\n\r\n')


def main():
    import socket
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('', 5000))
    serverSock.listen()

    try:
        while True:
            print('waiting connection...')
            clientSock, addr = serverSock.accept()
            print('connected from: <%s:%s>' % addr)
            while True:
                rqst = clientSock.recv(1024)
                if rqst:
                    print(type(rqst), rqst)
                else:
                    clientSock.close()
                    break
    except KeyboardInterrupt:
        if clientSock:
            clientSock.close()
        serverSock.close()


if __name__ == '__main__':
    main()
