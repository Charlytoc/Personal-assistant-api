from django.urls import path
from .views import say_hello_world, LoginView
app_name = 'authenticate'
urlpatterns = [
    path('hello/', say_hello_world, name='hello'),
    path('login', LoginView.as_view(), name='login'),
]