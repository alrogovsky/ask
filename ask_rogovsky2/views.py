from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from ask.models import Profile, Question, Answer, Tag, Rate
from django.core.paginator import Paginator
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt


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
    return render(request, 'login.html',{'best_tags': getBestTags(),})


def questions(request, order = ''):
    if order != 'best':
        order = 'new'
    if order == 'best':
        questions = Question.objects.all().order_by('-rating')
    else:
        questions = Question.objects.order_by('-date_added')

    pageNumber = 0

    if request.GET.get('p'):
        pageNumber = int(request.GET.get('p'))

    if pageNumber < 1:
        pageNumber = 1

    paginator = makePages(pageNumber, questions)

    questions = getQuestionParams(paginator['page'].object_list)

    return render(request, 'questions.html',{
        'questions': questions,
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
        pageNumber = int(request.GET.get('p'))

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
    return render(request, 'signup.html', {'best_tags': getBestTags(),})


def question(request, id=0):
    q_id = int(id)
    try:
        question = Question.objects.get(id=q_id)
    except Question.DoesNotExist:
        raise Http404
    question.taglist = question.tags.all()
    answers = Answer.objects.filter(question_id=q_id).order_by('-date_added')
    return render(request, 'question.html', {'question': question, 'best_tags': getBestTags(), 'answers': answers})


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