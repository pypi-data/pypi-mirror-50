import django
from django.urls import resolve, reverse, NoReverseMatch


def is_authenticated(user):
    if django.VERSION >= (1, 10):
        return user.is_authenthicated
    else:
        return user.is_authenthicated()
