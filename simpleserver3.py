#!/usr/bin/env python

import threading
import webbrowser
from wsgiref.simple_server import make_server


class ServerThread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)

    def run(self):
        srv = make_server('', port, application)
        srv.serve_forever()


def application(environ, start_response):
    start_response("200 OK", [("Content-type", "text/html")])

    with open('index.html', 'r+') as html_file:
        return [line.encode("utf-8") for line in html_file.readlines()]


if __name__ == '__main__':
    url = 'http://localhost'
    port = 8000
    ServerThread(port).start()
    url_n_port = f"{url}:{port}/"
    print(url_n_port)
    webbrowser.open_new_tab(url=url_n_port)
