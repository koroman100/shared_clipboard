import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import clipboard
import requests
import time

import threading

port = int(sys.argv[1])
global_clip_data = clipboard.paste()

class myHandler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        global global_clip_data

        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)

        global_clip_data = post_data.decode()

        clipboard.copy(global_clip_data)

        self._set_response()


def copy_detecter():

    global global_clip_data

    while True:
        time.sleep(1)

        new_data = clipboard.paste()

        server_list = open("shared_list.txt", "r").readlines()

        for server in server_list:
            if global_clip_data != new_data:
                global_clip_data = new_data

                try:
                   requests.post(server, data=global_clip_data.encode())
                   print("clip posted")
                except:
                   pass


copy_thread = threading.Thread(target=copy_detecter)
copy_thread.start()


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

server = ThreadingSimpleServer(("0.0.0.0", port), myHandler)

try:
    while True:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print("\nShutting down server per users request.")
