from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from ask.models import Profile, Question, Answer, Tag, Rate
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
    questions = Question.objects.all().order_by('-date_added')
    for q in questions:
        q.answers = Answer.objects.filter(question_id = q.id).count()
    return render(request, 'questions.html', {'questions':questions})


def signup(request):
	return render(request, 'signup.html')


def question(request, id=0):
    q_id = int(id)
    try:
        question = Question.objects.get(id = q_id)
    except Question.DoesNotExist:
        raise Http404
    answers = Answer.objects.filter(question_id=q_id).order_by('-date_added')
    return render(request, 'question.html', {'question':question, 'answers':answers})


def ask(request):
	return render(request, 'ask.html')
