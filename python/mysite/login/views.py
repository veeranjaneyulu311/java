from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User

# Create your views here.

def homePage(request):
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
			return HttpResponse("welcome Mr."+name)
		else:
			return HttpResponse("enter valid password")
	else:
		return HttpResponse("enter valid username")