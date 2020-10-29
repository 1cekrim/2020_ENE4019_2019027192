import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.client_address[0])
        buffer = self.request.recv(1024).strip()

        req = self.parse_http(buffer)

        if req['method'] == 'GET':
            rep = self.handle_get(req)
        
        self.send_response(rep)

        # self.request.send(html_text)

    def send_response(self, rep):
        print(rep)
        self.send_response(rep["code"])
        for key, val in rep['headers'].items():
            self.send_header(key, val)
        self.end_headers()
        self.wfile.write(rep["content"])

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
        file_path = f'./html/{filename}'
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
                print(html_text[:100].decode('utf-8'))
                input()
                result['headers']['Content-Length'] = len(result['content'])
                return result

        assert(false)

        

def main():
    server = socketserver.TCPServer(('0.0.0.0', 80), TCPHandler)
    server.serve_forever()

if __name__ =="__main__":
    main()