from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', mainPage, name='main_page_url'),
    path('match/', showMatchInfo, name='match_details_url' )
]