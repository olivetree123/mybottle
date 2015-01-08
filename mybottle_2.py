#coding:utf-8
#该文件用来备份前面的代码

from wsgiref.simple_server import make_server

class MyBottle:

    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        #print 'environ : ', self.environ
        for key in self.environ:
            print key,' : ',self.environ[key]
        path = self.environ['PATH_INFO']
        if path == "/":
            return self.GET_index()
        elif path == "/hello":
            return self.GET_hello()
        else:
            return self.notfound()

    def GET_index(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Welcome!\n"

    def GET_hello(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello world!\n"

    def notfound(self):
        status = '404 Not Found'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Not Found\n"


def route(path):
    def route1(func):
        def route2():
            return func
        return route2
    return route1


def run(app):
	# 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
	httpd = make_server('', 8000, app)
	print "Serving HTTP on port 8000..."
	# 开始监听HTTP请求:
	httpd.serve_forever()





if __name__ == '__main__':
    app = MyBottle()
	run(app)
