import datetime
import logging
import socket
import threading

from .consts import PAGE_404, HTTP_STATUS_MSGS

logger = logging.getLogger('Flamingo server')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s - %(message)s - %(threadName)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class Config:
    error_pages = {
        404: None
    }

class Session(threading.local):
    def __init__(self):
        super(Session, self).__init__()
        self.request = None

class Request:
    def __init__(self, data):
        self.raw = data
        self._parse()
        
    def _parse(self):
        i = self.raw.find("\r\n\r\n")
        if not i:
            raise Exception()
        head = self.raw[:i]
        self.body = self.raw[i+3:]
        head = head.split("\r\n")
        self.method, self.path, self.protocol = head[0].split(" ")
        self.headers = {}
        for h in head[1:]:
            split_i = h.find(":")
            if not split_i:
                raise Exception()
            self.headers[h[:split_i]] = h[split_i+1:].strip()

    def __repr__(self):
        return "Requets obj @ %s" % self.path

class Response:
    def __init__(self, code=200, content="", content_type=None):
        self.code = code
        self.headers = {}
        self.content = content
        if content_type:
            self.headers["Content-Type"] = content_type

    def _calcContentLength(self):
        self.headers["Content-Length"] = len(self.content)
    
    def _makeHeader(self):
        res = ""
        for h in self.headers:
            res += "%s: %s\r\n" % (h, self.headers[h])
        res += "\r\n"
        return res

    def prepare(self):
        self._calcContentLength()
        self.raw = "HTTP/1.1 %d %s\r\n" % (self.code, HTTP_STATUS_MSGS[self.code])
        self.raw += self._makeHeader()
        self.raw += self.content
        self.raw = self.raw.encode()
        

class Worker(threading.Thread):
    def __init__(self, conn, addr, registered_routes):
        super(Worker, self).__init__()
        self.conn = conn
        self.addr = addr
        self.BUFFER_SIZE = 1024
        self.registered_routes = registered_routes
        
    def _recv(self):
        data = b""
        while True:
            buffer = self.conn.recv(self.BUFFER_SIZE)
            data += buffer
            if len(buffer) < self.BUFFER_SIZE:
                break
        if not data:
            return False
        self.data = data.decode()
        return 1
        

    def run(self):
        if self._recv():
            global session
            req = Request(self.data)
            session.request = req
            if req.path in self.registered_routes.keys():
                context = self.registered_routes[req.path]
                
                if isinstance(context, Response):
                    res = context
                elif callable(context):
                    res = context()
                    if type(res) != Response:
                        res = Response(200, res)
                else:
                    res = Response(200, context)
            else:
                if Config.error_pages[404]:
                    err_code = Config.error_pages[404]
                else:
                    err_code = PAGE_404
                res = Response(404, err_code)

            res.prepare()
            self.conn.send(res.raw)

            logger.info("%s:%s '%s %s %s'" % (self.addr[0], self.addr[1], req.method, req.path, req.protocol))
        self.conn.close()
            

class Flamingo:
    def __init__(self):
        self.registered_routes = {}

    def register(self, path, context):
        self.registered_routes[path] = context            

    def run(self, host="127.0.0.1", port=8000, debug=False, n_listen=10):
        self.addr = (host, port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            logger.info("Server running at %s:%s" % self.addr)
            sock.bind(self.addr)
            sock.listen(n_listen)
            while True:
                conn, addr = sock.accept()
                thread = Worker(conn, addr, self.registered_routes)
                thread.start()


session = Session()

