from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from models import Question, Answer, UserProfile, Tag, LikeAnswer
from django.core.paginator import Paginator, Page
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
import logging
import datetime

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
        
def profile_edit_display(request):
        if not request.user.is_authenticated():
            raise PermissionDenied
            
        if request.method == 'POST':
            request_username = request.POST.get('username','')
            request_password = request.POST.get('password','')
            request_psw_confirm = request.POST.get('psw_confirm')
            request_email = request.POST.get('email')
            request_first_name = request.POST.get('first_name')
            request_last_name = request.POST.get('last_name')
            
            if request_password != request_psw_confirm:
                    return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '1',
                        'input_username': request_username,
                        'input_email': request_email,
                        'input_first_name': request_first_name,
                        'input_last_name': request_last_name,                        
                         })
             
            if request_username != request.user.username:
                if User.objects.filter(username = request_username).exists():
                    return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '2',
                        'input_username': request_username,
                        'input_email': request_email,
                        'input_first_name': request_first_name,
                        'input_last_name': request_last_name, 
                    
                     })
                    
            if request_email != request.user.email:
                if User.objects.filter(email = request_email).exists():
                    return render(request, 'profile_edit.html', {'page_title': 'Edit Profile', 'errors': '3', 
                        'input_username': request_username,
                        'input_email': request_email,
                        'input_first_name': request_first_name,
                        'input_last_name': request_last_name, 
                        
                        })
                
            current_user = request.user
            
            current_user.username = request_username
            current_user.email = request_email
            current_user.first_name = request_first_name
            current_user.last_name = request_last_name
            current_user.backend = 'django.contrib.auth.backends.ModelBackend'
            if request_password != '':
                current_user.set_password(request_password)
            
            current_user.save()
            
            new_user_session = auth.authenticate(username = request_username, password = request_password)
            auth.login(request, new_user_session)
            
            return HttpResponseRedirect(request.GET.get('continue', 'http://localhost/'))
        
        return render(request, 'profile_edit.html', {'page_title': 'Edit profile', 'errors': '0'})
            
        
def question_display(request, question_id):
        try:
            question = Question.objects.get_by_id(question_id)
        except:
            raise Http404
        
        if request.method == 'POST':
            request_text = request.POST.get('text')
            new_answer = Answer(text = request_text, 
                author = UserProfile.objects.get(user_account = request.user), 
                date = datetime.datetime.now(),
                question = Question.objects.get_by_id(question_id))
            
            new_answer.save()
            
            return HttpResponseRedirect('/question/{}/?p={}#{}'.format(question_id, request.GET.get('p',1), new_answer.id))
        
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
        if not request.user.is_authenticated():
            raise PermissionDenied

        if request.method == 'POST':

            request_title = request.POST.get('title')
            request_text = request.POST.get('text')
            request_tags = request.POST.get('tags')
            
            new_question = Question(title = request_title, 
                date = datetime.datetime.now(), 
                author = UserProfile.objects.get(user_account = request.user),
                text = request_text)
            
            new_question.save()
            
            for tag_str in request_tags.split(','):
                if Tag.objects.filter(name = tag_str).exists():
                    tag = Tag.objects.get(name = tag_str)
                    new_question.tags.add(tag)
                else:
                    new_tag = Tag(name = tag_str)
                    new_tag.save()
                    new_question.tags.add(new_tag)
            
            return HttpResponseRedirect('/question/{}'.format(new_question.id))
            
        return render(request, 'ask.html', {'page_title': 'New Question', 'errors': '0'})
        
def like_answer(request):
    if request.method == 'POST':
        request_answer_id = request.POST.get('answer_id')
        request_value = True
        if request.POST.get('value') == '0':
            request_value = False
        request_user = UserProfile.objects.get(user_account = request.user)
        
        request_answer = Answer.objects.get_by_id(request_answer_id)
        
        new_like = LikeAnswer(value = request_value, answer = request_answer, author = request_user)
        new_like.save()
        
        
        if request_value is True:
            return HttpResponse(request_answer.likes_count())
        else:
            return HttpResponse(request_answer.dislikes_count()) 
    
    return PermissionDenied
        

        

    
