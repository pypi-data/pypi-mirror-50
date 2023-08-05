import multiprocessing
import os
import re
import shutil
import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from .routes import routes

next_payload = None
next_status_code = -1
next_path_regex = None
last_request = None


'''
Based on the implementation of @tliron
https://gist.github.com/tliron/8e9757180506f25e46d9

'''


class TestHTTPServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = routes
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_HEAD(self):
        self.handle_method('HEAD')

    def do_GET(self):
        self.handle_method('GET')

    def do_POST(self):
        self.handle_method('POST')

    def do_PUT(self):
        self.handle_method('PUT')

    def do_DELETE(self):
        self.handle_method('DELETE')

    def get_route(self):
        for path, route in self.routes.items():
            if re.match(path, self.path):
                return route
        return None

    def get_payload(self):
        payload_len = int(self.headers['content-length'])
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload)
        return payload

    def check_for_next_response(self):
        global next_status_code
        global next_payload
        global next_path_regex
        global last_request

        if self.path == '/set-response':
            payload = self.get_payload()
            next_status_code = payload['status_code']
            next_payload = payload['payload']
            next_path_regex = re.compile(
                payload['path_regex']) if 'path_regex' in payload else None
            self.send_response(200)
            self.end_headers()
            return True
        elif self.path == '/clear-response':
            next_status_code = -1
            next_payload = None
            next_path_regex = None
            self.send_response(200)
            self.end_headers()
            return True
        elif self.path == '/last-request':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(last_request), 'utf-8'))
            return True
        return False

    def handle_method(self, method):
        global next_status_code
        global next_payload
        global last_request
        global next_path_regex

        if self.check_for_next_response():
            return

        last_request = {
            'method': method,
            'path': self.path,
            'payload': self.get_payload() if self.headers['content-length'] and int(self.headers['content-length']) > 0 else None
        }

        if (next_status_code > -1) and (not next_payload is None) and ((next_path_regex is None) or next_path_regex.search(self.path)):
            self.send_response(next_status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(next_payload), 'utf-8'))
        else:
            route = self.get_route()
            if route is None:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes('Route not found\n', 'utf-8'))
            else:
                if method == 'HEAD':
                    self.send_response(200)
                    if 'media_type' in route:
                        self.send_header('Content-type', route['media_type'])
                    self.end_headers()
                else:
                    if 'file' in route:
                        if method == 'GET':
                            try:
                                f = open(os.path.join(here, route['file']))
                                try:
                                    self.send_response(200)
                                    if 'media_type' in route:
                                        self.send_header(
                                            'Content-type', route['media_type'])
                                    self.end_headers()
                                    shutil.copyfileobj(f, self.wfile)
                                finally:
                                    f.close()
                            except:
                                self.send_response(404)
                                self.end_headers()
                                self.wfile.write(
                                    bytes('File not found\n', 'utf-8')
                                )
                        else:
                            self.send_response(405)
                            self.end_headers()
                            self.wfile.write(
                                bytes('Only GET is supported\n', 'utf-8')
                            )
                    else:
                        if method in route:
                            content = route[method](self)
                            if content is not None:
                                self.send_response(200)
                                if 'media_type' in route:
                                    self.send_header(
                                        'Content-type', route['media_type'])
                                self.end_headers()
                                if method != 'DELETE':
                                    self.wfile.write(
                                        bytes(json.dumps(content), 'utf-8'))
                            else:
                                self.send_response(404)
                                self.end_headers()
                                self.wfile.write(bytes('Not found\n', 'utf-8'))
                        else:
                            self.send_response(405)
                            self.end_headers()
                            self.wfile.write(
                                bytes(method + ' is not supported\n', 'utf-8'))


server_address = ('127.0.0.1', 2020)


def start_server():
    httpd = HTTPServer(server_address, TestHTTPServer)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def set_next_response(status_code, payload, path_regex=None):
    request = {'status_code': status_code, 'payload': payload}
    if path_regex is not None:
        request['path_regex'] = path_regex
    try:
        response = requests.post(
            url='http://%s:%d/set-response' % server_address,
            json=request
        )
        return response.status_code == 200
    except:
        pass


def clear_next_response():
    try:
        response = requests.post(
            url='http://%s:%d/clear-response' % server_address
        )
        return response.status_code == 200
    except:
        pass


def get_last_request():
    try:
        response = requests.get(
            url='http://%s:%d/last-request' % server_address
        )
        return response.json()
    except:
        pass


_process = None


def start():
    _process = multiprocessing.Process(target=start_server, args=())
    _process.daemon = True
    _process.start()


def stop():
    if not _process is None:
        _process.stop()
