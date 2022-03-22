# As a final step, create a file inside your catalog folder called urls.py, and add the following text to define
#  the (empty) imported urlpatterns. This is where we'll add our patterns as we build the application.

from django.urls import path
from . import views

urlpatterns = [
    path('rhchatbot/', views.chat, name='index')
]