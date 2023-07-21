from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
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
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if not email or not password:
            return HttpResponseBadRequest('Email and password must be provided.')

        # Try to find the user
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid email.')

        # Check if user is active
        if not user.is_active:
            return HttpResponseBadRequest('User account is inactive.')

        # Check the password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # User is authenticated. Replace the following dummy token with your actual logic.
            token = "dummy_token"
            return JsonResponse({'token': token})
        else:
            # Invalid password
            return HttpResponseBadRequest('Invalid password.')
