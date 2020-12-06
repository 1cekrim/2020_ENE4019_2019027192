import time
import ssl
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from urllib.parse import urlparse

template_dict = {}

class HTTPHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_POST(self):
        if self.request_version != self.protocol_version:
            self.handle_400()
            return

        post_len = int(self.headers['Content-Length'])
        post_data = self.rfile.read(post_len).decode('utf-8')

        qres = {}
        for q in post_data.split('&'):
            if '=' in q:
                s = q.split('=')
                qres[s[0]] = s[1]
        query = qres

        parsed_path=urlparse(self.path.strip().lower())
        path = parsed_path.path
        path = path.split('/')
        if not path[0]:
            path = path[1:]
        
        filename = path[0]
        if not filename:
            filename = 'index.html'
        file_path = f'./static/{filename}'
        extension = filename.split('.')[-1]

        import os.path
        if not os.path.exists(file_path):
            self.handle_404()
            return

        if extension == 'html':
            with open(file_path, 'r', encoding='utf8') as f:
                content = f.read()
            content, res = template_dict[file_path](content, query, 'POST')
            content = content.encode('utf-8')
            self.send_response(res)
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.handle_500()

    def do_PUT(self):
        self.do_POST()

    def do_GET(self):
        if self.request_version != self.protocol_version:
            self.handle_400()
            return

        parsed_path=urlparse(self.path.strip().lower())
        query = parsed_path.query
        qres = {}
        for q in query.split('&'):
            if '=' in q:
                s = q.split('=')
                qres[s[0]] = s[1]
        query = qres

        fullpath = parsed_path.path
        path = fullpath.split('/')
        if not path[0]:
            path = path[1:]
        
        filename = path[-1]
        if not filename:
            filename = 'index.html'

        fullpath = '/'.join(path)

        file_path = f'./static/{fullpath}'
        print(file_path)
        extension = filename.split('.')[-1]
        print(extension)

        import os.path
        if not os.path.exists(file_path):
            self.handle_404()
            return

        if extension == 'html':
            with open(file_path, 'r', encoding='utf8') as f:
                content = f.read()
            content, res = template_dict[file_path](content, query, 'GET')
            content = content.encode('utf-8')
            self.send_response(res)
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Type', 'text/html;charset=utf-8')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif extension == 'jpg':
            self.send_response(200)
            self.send_header('Referrer-Policy', 'no-referrer')
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_header('Content-Type', 'image/jpg')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            
        elif extension == 'png':
            self.send_response(200)
            self.send_header('Referrer-Policy', 'no-referrer')
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        else:
            self.handle_500()

    def handle_400(self):
        self.send_response(400)
        content = '<html><body>400 Bad Request</body><html>'
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_404(self):
        self.send_response(404)
        content = '<html><body>404 Not Found</body><html>'
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def handle_500(self):
        self.send_response(500)
        content = '<html><body>500 Internal Server Error</body><html>'
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content.encode())

    def parse_http(self, text):
        text = text.decode('utf-8')
        req = {}
        req['split'] = text.split('\r\n')
        meta = req['split'][0].split(' ')
        req['method'] = meta[0]
        req['path'] = meta[1]
        req['version'] = meta[2]
        req['headers'] = {}

        for header in req['split'][1:]:
            key, val = header.split(': ')
            req['headers'][key] = val

        return req

    def handle_get(self, req):
        import time
        result = {}
        result['headers'] = {}
        result['version'] = req['version']
        result['headers']['Content-Type'] = 'text/html; charset=UTF-8'
        result['headers']['Referrer-Policy'] = 'no-referrer'
        tm = time.time()
        result['headers']['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S') + ' KST'

        if req['version'] != 'HTTP/1.1':
            result['code'] = 400
            result['code_name'] = 'Bad Request'
            result['content'] = '<html><body>400 Bad Request</body><html>'
            result['headers']['Content-Length'] = len(result['content'])
            return result

        path = req['path'].split('/')

        if not path[0]:
            path = path[1:]
        # TODO: 파일 이름 하나만 설정
        filename = path[0]
        if not filename:
            filename = 'index.html'
        file_path = f'./static/{filename}'
        extension = filename.split('.')[-1]

        if extension == 'html':
            result['headers']['Content-Type'] = 'text/html; charset=UTF-8'
        elif extension == 'jpg':
            result['headers']['Content-Type'] = 'image/jpeg;'

        import os.path
        if not os.path.exists(file_path):
            result['code'] = 404
            result['code_name'] = 'Not Found'
            result['content'] = '<html><body>404 Not Found</body><html>'
            result['headers']['Content-Length'] = len(result['content'])
            return result

        if result['headers']['Content-Type'] == 'text/html; charset=UTF-8':
            with open(file_path, 'r') as f:
                    html_text = f.read()
                    result['code'] = 200
                    result['code_name'] = 'OK'
                    result['content'] = html_text
                    result['headers']['Content-Length'] = len(result['content'])
                    return result

        if result['headers']['Content-Type'] == 'image/jpeg;':
            with open(file_path, 'rb') as f:
                html_text = f.read()
                result['code'] = 200
                result['code_name'] = 'OK'
                result['content'] = html_text
                result['headers']['Content-Length'] = len(result['content'])
                return result

def start_server():
    server = ThreadingHTTPServer(('', 5253), HTTPHandler)
    server.socket = ssl.wrap_socket(server.socket, certfile='server.crt', keyfile='server.key', server_side=True)
    ip, port = server.server_address
    server.serve_forever()