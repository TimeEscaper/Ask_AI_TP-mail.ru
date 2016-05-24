"""ask_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from wsgi_view import views as wsgi_script
from read_only import views as read_only
from django.contrib.auth import views as auth_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^wsgi_test/$', wsgi_script.hello_wsgi),
    url(r'^$', read_only.index_display, name='index'),
    url(r'^hot/$', read_only.hot_display, name='hot'),
    url(r'^login/$',read_only.login_display, name='login'),
   # url(r'^login/$', auth_view.login, {'template_name':'login.html'}),
    url(r'^logout/$', read_only.logout_display, name='logout'),
    url(r'^signup/$',read_only.signup_display, name='signup'),
    url(r'^ask/$',read_only.ask_display, name='ask'),
    url(r'^tag/(?P<tag>\S+)/$',read_only.tag_display, name='tag_view'),
    url(r'^question/(?P<question_id>\d+)/$',read_only.question_display, name='question_view'),
]
