def winston(req, rep):
    if req:
        pass

    rep.set_headers([('Content-Type', 'text/html; charset=utf-8')])
    with open('index.html', 'r') as html:
        rep.start_response('200 OK', html.read())
    # rep.start_response('200 OK', '<h1>Hello,world</h1>')


def main():
    import socket
    from request import Request
    from response import Response

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('', 5000))
    serverSock.listen()

    try:
        while True:
            # receive request
            print('waiting connection...')
            clientSock, addr = serverSock.accept()
            print('connected from: <%s:%s>' % addr)
            rqst = Request(clientSock.recv(1024))

            rep = Response(clientSock)

            # analyze and handle request
            winston(rqst, rep)
            # construct and return response
            clientSock.close()
    except Exception:
        if clientSock:
            clientSock.close()
        serverSock.close()


if __name__ == '__main__':
    main()
