from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import auth
from ask.models import Profile, Question, Answer, Tag, Rate, Rate_Answer
from django.core.paginator import Paginator
from django.http import Http404
from ask_rogovsky2.forms import SignUp, EditProfile, Ask, AnswerForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os
import json as simplejson
from django.db.models import F


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

    Answer.objects.filter(id=request.POST['id']).update(rating = F('rating') + 1)
    return HttpResponse(html)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    redirect = "/"
    if request.GET.get('next'):
        redirect = request.GET.get('next')

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return render(request, 'login.html', {
                'best': getBest(),
                'username': username,
                'password': password,
                'error': 1,
                'redirect': redirect
            })
    return render(request, 'login.html', {'best': getBest(), 'redirect': redirect,})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next'))


def questions(request, order = ''):
    userpic = 0
    if order != 'best':
        order = 'new'
    if order == 'best':
        questions = Question.objects.all().order_by('-rating')
    else:
        questions = Question.objects.order_by('-date_added')

    pageNumber = 0

    if request.GET.get('p'):
        try:
            pageNumber = int(request.GET.get('p'))
        except ValueError:
            raise Http404

    if pageNumber < 1:
        pageNumber = 1

    paginator = makePages(pageNumber, questions)
    page_questions = getQuestionParams(paginator['page'].object_list)

    for q in page_questions:
        q.userpic = Profile.objects.get(user = q.author).avatar_url

    if request.user.is_authenticated():
        userpic = Profile.objects.get(user=int(request.user.id)).avatar_url

    return render(request, 'questions.html',{
        'questions': page_questions,
        'best': getBest(),
        'order':order,
        'pagesRange': paginator['pagesRange'],
        'lastPage': paginator['lastPage'],
        'currentPage': pageNumber,
        'userpic': userpic,
    })


def bytag(request, tag=''):
    userpic = 0
    t = Tag.objects.get(word=tag)
    questions = t.question_set.all().order_by('-date_added')

    pageNumber = 0

    if request.GET.get('p'):
        try:
            pageNumber = int(request.GET.get('p'))
        except ValueError:
            raise Http404

    if pageNumber < 1:
        pageNumber = 1

    paginator = makePages(pageNumber, questions)

    questions = getQuestionParams(paginator['page'].object_list)

    for q in questions:
        q.userpic = Profile.objects.get(user = q.author).avatar_url
        print q.userpic

    if request.user.is_authenticated():
        userpic = Profile.objects.get(user=int(request.user.id)).avatar_url

    return render(request, 'questions.html', {
        'questions': questions,
        'best': getBest(),
        'tag': tag,
        'pagesRange': paginator['pagesRange'],
        'lastPage': paginator['lastPage'],
        'currentPage': pageNumber,
        'userpic': userpic
    })


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = SignUp(request.POST, request.FILES)
        if form.is_valid():
            usr = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['pass1'])
            prof = Profile.objects.create(rating=0, user_id=usr.id)
            if(request.FILES):
                prof.avatar_url = request.FILES['avatar']
                prof.save()
            return HttpResponseRedirect("/")
    else:
        form = SignUp()
    return render(request, 'signup.html', {'best': getBest(), 'form':form, })


@login_required(login_url='/login/')
def profile_edit(request):
    userpic = Profile.objects.get(user=int(request.user.id)).avatar_url
    form = EditProfile()
    ava = Profile.objects.get(user=int(request.user.id)).avatar_url
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['name']
            request.user.last_name = form.cleaned_data['l_name']
            if form.cleaned_data['email'] != '':
                request.user.email = form.cleaned_data['email']
            request.user.save()
            if request.FILES:
                prof = Profile.objects.get(user=int(request.user.id))
                prof.avatar_url = request.FILES['avatar']
                prof.save()
            ava = Profile.objects.get(user=int(request.user.id)).avatar_url
        return render(request, 'edit.html', {'best':getBest(), 'form':form, 'ava': ava, 'success': 1, 'userpic': userpic})
    else:
        return render(request, 'edit.html', {'best':getBest(), 'form':form, 'ava': ava, 'userpic': userpic})


def question(request, id=0):
    userpic = 0
    form = AnswerForm()
    if request.user.is_authenticated():
        userpic = Profile.objects.get(user=int(request.user.id)).avatar_url
    q_id = int(id)
    try:
        question = Question.objects.get(id=q_id)
    except Question.DoesNotExist:
        raise Http404

    answers = Answer.objects.filter(question_id=q_id).order_by('date_added')

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.question = question
            a.author = request.user
            a.save()
            return HttpResponseRedirect('/question/' + str(q_id) + '#answer' + str(answers.count()) )

    question.taglist = question.tags.all()
    question.userpic = Profile.objects.get(user = question.author).avatar_url


    for an in answers:
        an.userpic = Profile.objects.get(user=an.author).avatar_url

    return render(request, 'question.html', {
        'question': question,
        'best': getBest(),
        'answers': answers,
        'userpic': userpic,
        'form': form
    })


@login_required(login_url='/login/')
def ask(request):
    userpic = 0
    if request.user.is_authenticated():
        userpic = Profile.objects.get(user=int(request.user.id)).avatar_url

    if request.method == 'POST':
        form = Ask(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                rating=0,
                author=request.user
            )
            tag_list = form.cleaned_data['tags'].split(",")
            for x in tag_list[:3]:
                if x.strip() != "":
                    try:
                        tag = Tag.objects.get(word = x.strip())
                    except Tag.DoesNotExist:
                        tag = Tag.objects.create(word = x.strip())
                    question.tags.add(tag)
            question.save()
            return HttpResponseRedirect("/question/" + str(question.id))
    else:
        form = Ask()
    return render(request, 'ask.html',{'best': getBest(), 'userpic': userpic, 'form': form})


def rate(request):
    if request.user.is_authenticated():
        if request.method == 'POST' and 'action' in request.POST and 'id' in request.POST and 'type' in request.POST:
            if request.POST['type'] == 'answer':
                try:
                    Rate_Answer.objects.get(answer_id = request.POST['id'], user_id = request.user.id)
                    response = {
                        'result': 'exists',
                    }
                    jsondata = simplejson.dumps(response)
                    return HttpResponse(jsondata,content_type='application/json')
                except Rate_Answer.DoesNotExist:
                    print request.POST['id']
                    if request.POST['action'] == 'like':
                        Answer.objects.filter(id=request.POST['id']).update(rating = F('rating') + 1)
                    if request.POST['action'] == 'dislike':
                        Answer.objects.filter(id=request.POST['id']).update(rating = F('rating') - 1)
                    Rate_Answer.objects.create(answer_id = request.POST['id'], user_id = request.user.id)
                    response = {
                        'result': 'done',
                        'new': Answer.objects.get(id=request.POST['id']).rating
                    }
                    jsondata = simplejson.dumps(response)
                    return HttpResponse(jsondata,content_type='application/json')
            if request.POST['type'] == 'question':
                try:
                    Rate.objects.get(question_id = request.POST['id'], user_id = request.user.id)
                    response = {
                        'result': 'exists',
                    }
                    jsondata = simplejson.dumps(response)
                    return HttpResponse(jsondata,content_type='application/json')
                except Rate.DoesNotExist:
                    print request.POST['id']
                    if request.POST['action'] == 'like':
                        Question.objects.filter(id=request.POST['id']).update(rating = F('rating') + 1)
                    if request.POST['action'] == 'dislike':
                        Question.objects.filter(id=request.POST['id']).update(rating = F('rating') - 1)
                    Rate.objects.create(question_id = request.POST['id'], user_id = request.user.id)
                    response = {
                        'result': 'done',
                        'new': Question.objects.get(id=request.POST['id']).rating
                    }
                    jsondata = simplejson.dumps(response)
                    return HttpResponse(jsondata,content_type='application/json')
        else:
            raise Http404
    else:
        response = {
                        'result': 'login',
                    }
        jsondata = simplejson.dumps(response)
        return HttpResponse(jsondata,content_type='application/json')

########### helpers #############
def getQuestionParams(questions):
    for q in questions:
        q.answers = Answer.objects.filter(question_id=q.id).count()
        q.taglist = q.tags.all()
    return questions


def getBest():
    tags = Tag.objects.all()
    i=1
    colors = {1:'label-primary', 2:'label-success', 3:'label-info', 4:'label-warning', 5:'label-danger'}
    for t in tags:
        t.quantity = t.question_set.all().count()
    tags = sorted(tags, key=lambda x: x.quantity, reverse=True)
    tags = tags[:5]

    for t in tags:
        t.color = colors[i]
        i+=1

    best_users = Profile.objects.order_by('-rating')[:5]
    for u in best_users:
        u.username = u.user.username
    return {'tags': tags, 'best_users': best_users}
    


def makePages(pageNumber, questions):
    p = Paginator(questions, 10)
    lastPage = p.num_pages

    if pageNumber > lastPage:
        pageNumber = lastPage

    page = p.page(pageNumber)

    if pageNumber < 3:
        pagesStart = 1
    else:
        pagesStart = pageNumber - 2

    if (pagesStart + 5) > lastPage:
        pagesEnd = lastPage
        pagesStart = pagesEnd - 5
        if pagesStart < 1:
            pagesStart = 1
    else:
        pagesEnd = pagesStart + 5

    pagesRange = range(pagesStart, pagesEnd+1)

    return {'lastPage': lastPage, 'pagesRange': pagesRange, 'page': page}