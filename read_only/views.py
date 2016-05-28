from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from models import Question, Answer, UserProfile
from django.core.paginator import Paginator, Page
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
import logging

# Create your views here.

def index_display(request):
    question_list = Question.objects.get_new()
    page_n = request.GET.get('p',1)
    
    paginator = Paginator(question_list, 5)
    paginator.baseurl = 'http://localhost/?p='
    
    try:
        page_objects = paginator.page(page_n)
    except:
        raise Http404
    
    return render(request, 'index.html', {
       # 'question_list': paginator.object_list,
        'page_title': 'Index', 
        'paginator': paginator,
        'page_objects': page_objects,
    })
    
def hot_display(request):
    question_list = Question.objects.get_hot()
    page_n = request.GET.get('p',1)
    
    paginator = Paginator(question_list, 5)
    paginator.baseurl = 'http://localhost/hot/?p='
    
    try:
        page_objects = paginator.page(page_n)
    except:
        raise Http404
    
    return render(request, 'hot.html', {
       # 'question_list': paginator.object_list,
        'page_title': 'Popular questions', 
        'paginator': paginator,
        'page_objects': page_objects,
    })
    
#@csrf_protect
def login_display(request):
        if request.method == 'POST':
            request_username = request.POST.get('username','')
            request_password = request.POST.get('password','')
            request_user = auth.authenticate(username = request_username, password = request_password)
            if request_user is not None:
                auth.login(request, request_user)
               # return render(request, 'login.html', {'page_title': 'Log In', 'errors': '0'})
                return HttpResponseRedirect(request.GET.get('continue','http://localhost/'))
            else: 
                return render(request, 'login.html', {'page_title': 'Log In', 'errors': '1'})
                
        return render(request, 'login.html', {'page_title': 'Log In', 'errors': '0'})
        
def logout_display(request):
        if request.user.is_authenticated():
            auth.logout(request)
        return HttpResponseRedirect(request.GET.get('continue', 'http://localhost/'))
        
def signup_display(request):
        #return render(request, 'signup.html', {'page_title': 'Sign Up', })
        if request.method == 'POST':
            request_username = request.POST.get('username','')
            request_password = request.POST.get('password','')
            request_psw_confirm = request.POST.get('psw_confirm')
            request_email = request.POST.get('email')
            
            if request_password != request_psw_confirm:
                return render(request, 'signup.html', {'page_title': 'Sign Up', 'errors': '1' })
                
            if User.objects.filter(username = request_username).exists() or User.objects.filter(email = request_email).exists():
                return render(request, 'signup.html', {'page_title': 'Sign Up', 'errors': '2' })
                
            new_user = User.objects.create_user(request_username, request_email, request_password)
            new_user.save()
            new_profile = UserProfile(user_account = new_user, username = new_user.username, avatar = 'http://lorempixel.com/60/60/')
            new_profile.save()
            
            new_user_session = auth.authenticate(username = request_username, password = request_password)
            auth.login(request, new_user_session)
            
            return HttpResponseRedirect(request.GET.get('continue', 'http://localhost/'))
            
            
        return render(request, 'signup.html', {'page_title': 'Sign Up', 'errors': '0'})
            
        
def question_display(request, question_id):
        try:
            question = Question.objects.get_by_id(question_id)
        except:
            raise Http404
        
        answer_list = Answer.objects.get_by_question(question) 
        
        page_n = request.GET.get('p',1)
    
        paginator = Paginator(answer_list, 5)
        paginator.baseurl = 'http://localhost/question/{}/?p='.format(question_id)
    
        try:
            page_objects = paginator.page(page_n)
        except:
            raise Http404
    
        
        return render(request, 'question.html', {
            'question': question,
            'page_objects': page_objects,
            'page_title': 'Question',
            'paginator': paginator,
        })
        
def tag_display(request, tag):
        question_list = Question.objects.get_by_tag(tag)
        
        if (question_list.count() == 0):
            raise Http404
            
        page_n = request.GET.get('p',1)
    
        paginator = Paginator(question_list, 5)
        paginator.baseurl = 'http://localhost/tag/?p='
    
        try:
            page_objects = paginator.page(page_n)
        except:
            raise Http404
    
        return render(request, 'tag.html', {
            'tag': tag,
            'paginator': paginator,
            'page_objects': page_objects,
            'page_title': 'Tag: {}'.format(tag),
        })
        
def ask_display(request):
        return render(request, 'ask.html', {'page_title': 'New Question', })
        

        

    
