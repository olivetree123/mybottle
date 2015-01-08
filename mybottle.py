#coding:utf-8
import re,mimetypes
from cgi import parse_qs, escape
from jinja2 import Environment, PackageLoader 
from wsgiref.simple_server import make_server


class MyBottle:
    def __init__(self,urls):
        self.urls = {}
        for key in urls.keys():
            url = key
            if url[0] != '^':   url = '^'+url
            if url[-1] != '$':  url = url+'$'
            if url[-2] != '/':  url = url[:-1]+'/$'
            self.urls[url] = urls[key]
        self.urls['/static/(.*)/'] = get_static
        self.request = {'forms':{}}

    def __call__(self,environ, start_response):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        if path[-1] != '/': path = path+'/'
        print 'path : ',path
        d = parse_qs(environ['QUERY_STRING'])
        for k in d:
            d[k] = d[k][0] if d[k] else ''
        self.request['forms'] = d
        response_body,content_type = '','text/plain'
        for url in self.urls:
            m = re.match(url,path)
            if m:
                args = list(m.groups())
                args = [self.request]+args
                func = self.urls[url]
                response = func(*args)
                if isinstance(response,list):
                    response_body,content_type = response[0],response[1]
                else:
                    response_body = response
                break
        status = '200 OK'
        response_headers = [('Content-Type', content_type),('Content-Length', str(len(response_body)))]
        start_response(status,response_headers)
        return [response_body]

def get_static(request,file_path):
    return template(file_path)

def template(file_path):
    content = ''
    with open(file_path) as f:
        content = f.read()
    tp = mimetypes.guess_type(file_path)
    return [content,tp[0]]

def render(file_path = '',variables = ''):
    #variables 本应为字典，但是函数参数的默认值最好不要为可变对象
    env = Environment(loader=PackageLoader('mybottle', 'templates'))
    t = env.get_template(file_path)
    variables = {} if not variables else variables
    content = t.render(**variables)
    tp = mimetypes.guess_type(file_path)
    return [str(content),tp[0]]


def run(app):
	# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
	httpd = make_server('', 8000, app)
	print "Serving HTTP on port 8000..."
	# 开始监听HTTP请求:
	httpd.serve_forever()

