from django.contrib import admin
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', login),
    path('login', login),
    path('logout_view', logout_view),
    path('signup', signup),
    path('home', home),
    path('readerhome', readerhome),
    path('readers', readers),
    path('readers_list', readers_list),
    path('books', books),
    path('books_list', books_list),
    path('readerbooks_list', readerbooks_list),
    path('readerbooks', readerbooks),
    path('returns', returns),
    path('bookIssue', bookIssue),
    path('readerbookIssue', readerbookIssue),
    path('issuedbooks_list', issuedbooks_list),
    path('readerissuedbooks_list', readerissuedbooks_list),
    path('defaulter', defaulter),
    path('readerReport', readerReport),
    path('get_reader_info/', get_reader_info, name='get_reader_info'),
    path('get_book_info/', get_book_info, name='get_book_info'),
]
