from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import auth
from ask.models import Profile, Question, Answer, Tag, Rate
from django.core.paginator import Paginator
from django.http import Http404
from ask_rogovsky2.forms import SignUp, EditProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import os


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

    if int(request.GET.get('persist')) == 1:
        u = User.objects.get(pk = 1)
        t = Tag.objects.all()
        for x in range (1, 100):
            q = Question(author = u, title = 'GENERATED FOR TESTS', text = 'THIS IS GENERATED QUESTION!', date_added = "NOW()", rating = 0)
            q.save()
            q.tags.add(t[0])
            q.tags.add(t[1])
            q.tags.add(t[2])

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
                'best_tags': getBestTags(),
                'username': username,
                'password': password,
                'error': 1,
                'redirect': redirect
            })
    return render(request, 'login.html', {'best_tags': getBestTags(), 'redirect': redirect})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next'))


def questions(request, order = ''):
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

    return render(request, 'questions.html',{
        'questions': page_questions,
        'best_tags': getBestTags(),
        'order':order,
        'pagesRange': paginator['pagesRange'],
        'lastPage': paginator['lastPage'],
        'currentPage': pageNumber
    })


def bytag(request, tag=''):
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

    return render(request, 'questions.html', {
        'questions': questions,
        'best_tags': getBestTags(),
        'tag': tag,
        'pagesRange': paginator['pagesRange'],
        'lastPage': paginator['lastPage'],
        'currentPage': pageNumber
    })


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = SignUp(request.POST, request.FILES)
        if form.is_valid():
            usr = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['pass1'])
            request.FILES['avatar'].name = usr.username + "/" + request.FILES['avatar'].name
            print request.FILES['avatar'].name
            prof = Profile.objects.create(rating=0, user_id=usr.id, avatar_url = request.FILES['avatar'])
            return HttpResponseRedirect("/")
    else:
        form = SignUp()
    return render(request, 'signup.html', {'best_tags': getBestTags(), 'form':form, })


@login_required(login_url='/login/')
def profile_edit(request):
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
            return render(request, 'edit.html', {'best_tags':getBestTags(), 'form':form, 'ava': ava, 'success':1})
    else:
        return render(request, 'edit.html', {'best_tags':getBestTags(), 'form':form, 'ava': ava})


def question(request, id=0):
    q_id = int(id)
    try:
        question = Question.objects.get(id=q_id)
    except Question.DoesNotExist:
        raise Http404
    question.taglist = question.tags.all()
    answers = Answer.objects.filter(question_id=q_id).order_by('date_added')
    return render(request, 'question.html', {
        'question': question,
        'best_tags': getBestTags(),
        'answers': answers,
    })


def ask(request):
    getBestTags()
    return render(request, 'ask.html',{'best_tags': getBestTags()})


########### helpers #############
def getQuestionParams(questions):
    for q in questions:
        q.answers = Answer.objects.filter(question_id=q.id).count()
        q.taglist = q.tags.all()
    return questions


def getBestTags():
    tags = Tag.objects.all()
    i=1
    colors = {1:'label-primary', 2:'label-success', 3:'label-info', 4:'label-warning', 5:'label-danger'}
    for t in tags:
        t.quantity = t.question_set.all().count()
        t.color = colors[i]
        i += 1
    tags = sorted(tags, key=lambda x: x.quantity, reverse=True)
    return tags[:5]


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