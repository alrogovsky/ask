from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import hashlib
import os
import json as simplejson

@csrf_exempt
def helloworld(request):
	output = '<b>Hello World</b><br />'
	if request.method == 'GET':
		output += 'Get query: '
		for x in request.GET:
			output += x + '='
			output += request.GET[x] + ' '
	else:
		output += 'Post query: '
		for x in request.POST:
			output += x + '='
			output += request.POST[x] + ' '
	html = "<html><body>%s</body></html>" % output
	return HttpResponse(html)

def login(request):
	return render(request, 'login.html')

def questions(request):
	users = [
	{
		"name": "Vasya",
	},
	{
		"name": "admin",
	}

	]
	return render(request, 'questions.html', {"users": users})

def signup(request):
	return render(request, 'signup.html')

def question(request, id=0):
	return render(request, 'question.html')

def ask(request):
	return render(request, 'ask.html')
