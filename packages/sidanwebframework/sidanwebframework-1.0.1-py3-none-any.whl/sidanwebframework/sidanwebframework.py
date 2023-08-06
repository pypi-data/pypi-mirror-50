from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from json import dumps, loads
from os import getcwd

path_arr = []

class Serv(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        SetCorsHeaders(self)
        self.end_headers()


    def do_POST(self):
        ProcessUrl(self, 'POST')


    def do_GET(self):
        if len(path_arr) == 0:
            response = "\
                <html>\
                    <head>\
                        <title>sidanwebframework</title>\
                    </head>\
                    <body>\
                    <h2>\
                        sidanwebframework is successfully\
                        running\
                    </h2>\
                    </body>\
                </html>"
            self.send_response(200)
            SendResponse(self, response)
        ProcessUrl(self, 'GET')
    
    
    def do_PUT(self):
        ProcessUrl(self, 'PUT')
    
    
    def do_DELETE(self):
        ProcessUrl(self, 'DELETE')
        

class Request:

    def __init__(self, method, headers, body, params):
        self.method = method
        self.headers = headers
        self.body = body
        self.params = params


class Route:

    def __init__(self, path, function):
        self.path = path
        self.function = function


class Server:

    def __init__(self, ip='127.0.0.1', port=8080):
        self.ip = ip
        self.port = port


    def serve(self):
        """ ``serve()`` call this method to start the server."""
        try:
            httpd = HTTPServer((self.ip, self.port), Serv)
            link = 'http://{}:{}'.format(self.ip, self.port)
            print('server running at ' + link)
            httpd.serve_forever()
            return True
        except:
            httpd.socket.close()
            print('Server stopped')


def SetCorsHeaders(self):  # cors headers
    self.send_header('Access-Control-Allow-Credentials', 'true')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-type')


def route(path):
    """
    ``@route()`` use this decorator to define the route, pass path as argument
    """
    def wrap(func):
        path_obj = Route(path, func)
        path_arr.append(path_obj)
    return wrap


def ProcessUrl(self, method):
    query = urlparse(self.path).query
    url_params = {}
    if len(query) > 1:
        url_params = dict(qc.split('=') for qc in query.split('&'))
    path = self.path
    if self.path.find('?') != -1:
        path = self.path[0:self.path.find('?')]
    flag = 0
    for obj in path_arr:
        if obj.path == path:
            req_body = {}
            if self.headers.get('Content-Length') is not None:
                req_body = self.rfile.read(int(self.headers.get('Content-Length')))
            if len(req_body) > 0:
                if self.headers.get('Content-Type') == 'application/json':
                    req_body = loads(req_body)
                else:
                    req_body = req_body.decode("utf-8")
                    req_body = dict(qc.split('=') for qc in req_body.split('&'))
            req_obj = Request(method, self.headers, req_body, url_params)
            response = obj.function(req_obj)
            if response is None:
                response = '{} does have return statement'.format(obj.path)
            self.send_response(200)
            SetCorsHeaders(self)  # to set cors headers
            SendResponse(self, response)
            return True
        flag = flag + 1
        if flag == len(path_arr):
            self.send_response(404)
            SendResponse("Path not found")


def Response(data):
    """``Response()`` return this function with arguments, the arguments can be JSON type or String."""
    try:
        if type(data) == dict:
            return dumps(data)
        return str(data)
    except:
        return data


def Render(FilePath, context={}):
    """ ``Render()`` render the html document with given optional context  """
    try:
        file_obj = open(getcwd() + '/' + FilePath)
        data = file_obj.read()
        keys = list(context.keys())
        to_replace = []
        for index, char in enumerate(data):
            if char == '{':
                if data[index+1] == '{':
                    start = index
            if char == '}':
                if data[index+1] == '}':
                    stop = index
                    if data[start+2:stop] in keys:
                        rp_obj = {
                            "key": data[start-1:stop+2],
                            "value": context[keys[keys.index(data[start+2:stop])]]
                        }
                        to_replace.append(rp_obj)
                    else:
                        rp_obj = {
                            "key": data[start-1:stop+2],
                            "value": ""
                        }
                        to_replace.append(rp_obj)
        for obj in to_replace:
            data = data.replace(obj['key'], str(obj['value']))
        file_obj.close()
        return data
    except Exception as e:
        return str(e)


def SendResponse(self, response):
    try:
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))
    except:
        self.end_headers()
        response = str(response)
        response = dumps(response)
        self.wfile.write(bytes(response, 'utf-8'))