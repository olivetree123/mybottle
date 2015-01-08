#coding:utf-8

from mybottle import MyBottle,run,template,render

def index(request):
	return 'hello'

def hello(request,name = 'mmm'):
	#return template('templates/hello.html')
	return render('hello.html',{'name':'qqq'})

urls = {r'^/$':index,r'^/hello/(\w+)$':hello}

if __name__ == '__main__':
	app = MyBottle(urls = urls)
	run(app)
