from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User

# Create your views here.

def homePage(request):
	print(list(request))
	template = loader.get_template('login/home.html')
	context = {}
	return HttpResponse(template.render(context,request))
	
def userlogin(request):
	template = loader.get_template('login/login.html')
	context = {}
	return HttpResponse(template.render(context,request))

def uservalidation(request):
	name=request.POST['nm']
	print(name)
	pwd=request.POST['pwd']
	nameList=list(User.objects.all().values_list('user_name',flat=True))
	if name in nameList:
		us=User.objects.get(user_name=name)
		if us.pwd==pwd :
			return HttpResponse("<h2 style='color:green'>welcome Mr."+name+"</h2><br><b><a href='/login'>Login</a></b>")
		else:
			return HttpResponse("<h2 style='color:red'>enter valid password Mr."+name+"</h2><br><b><a href='/login'>Login</a></b>")
	else:
		return HttpResponse("<h2 style='color:red'>enter valid username</h2><br><b><a href='/login'>Login</a></b>")