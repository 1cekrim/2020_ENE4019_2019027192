import time
from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer

class HTTPHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_POST(self):
        if self.request_version != self.protocol_version:
            self.handle_400()
            return
        self.send_response(200)
        self.send_header('Referrer-Policy', 'no-referrer')
        self.end_headers()
        clen = int(self.headers.getheader('Content-Length', 0))
        body = self.rfile.read(clen)
        self.wfile.write(f'[receive]</br>{body}')

    def do_PUT(self):
        self.do_POST()

    def do_GET(self):
        if self.request_version != self.protocol_version:
            self.handle_400()
            return

        path = self.path.strip().lower()
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

        self.send_response(200)
        self.send_header('Referrer-Policy', 'no-referrer')
        
        if extension == 'html':
            with open(file_path, 'r') as f:
                content = f.read()
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content.encode())

        elif extension == 'jpg':
            with open(file_path, 'rb') as f:
                content = f.read()
            self.send_header('Content-Type', 'image/jpg')
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

def main():
    server = ThreadingHTTPServer(('', 5253), HTTPHandler)
    ip, port = server.server_address
    print(f'{ip}:{port}')
    server.serve_forever()

if __name__ =="__main__":
    main()