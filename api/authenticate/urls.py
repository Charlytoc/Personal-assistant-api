from django.urls import path
from .views import say_hello_world
app_name = 'authenticate'
urlpatterns = [
    path('hello/', say_hello_world, name='hello'),
]