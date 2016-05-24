from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_wsgi(request):
    get_string = '<br>'.join(['%s=%s' % param for param in request.GET.items()]) 
    post_string = '<br>'.join(['%s=%s<br>' % param for param in request.POST.items()])
    body = 'Hello, World!<br><br>POST data:<br>%s<br>GET data:<br>%s<br>' % (post_string, get_string)
    
    return HttpResponse(body)
