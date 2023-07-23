from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .actions import get_or_create_valid_token


import json
# Create your views here.
def say_hello_world(request):
    return HttpResponse("Hello, world")


from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.views import View


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        # email = request.POST.get('email')
        password = data.get('password')
        email = data.get('email')
        # print(f'This is the email:{email} and this is the password: {password}')

        if not email or not password:
            return HttpResponseBadRequest('Email and password must be provided.')

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid email.')

        # Check the password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            token = get_or_create_valid_token(user)
            # User is authenticated. Replace the following dummy token with your actual logic.

            return JsonResponse({'token': token.key})
        else:
            # Invalid password
            return HttpResponseBadRequest('Invalid password.')
