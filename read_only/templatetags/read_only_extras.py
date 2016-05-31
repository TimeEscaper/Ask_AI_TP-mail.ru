from django import template

register = template.Library()

from read_only.models import Answer, UserProfile
from django.contrib.auth.models import User


@register.filter(name = 'user_liked_answer')
def user_liked_answer(answer, user):
    return answer.user_liked(user)
