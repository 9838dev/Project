from django.urls import path
from .views import *
urlpatterns = [
    path('',hello,name = 'hello'),
    path('register',register,name = 'register'),
    path('news',news,name='news'),
    path('faq',faq,name="faq"),
    path('terms',terms,name='terms')
]
