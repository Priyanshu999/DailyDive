from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import CreateView, View, TemplateView
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

class SignupView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Get user input from the custom form
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            # Handle password mismatch error
            return render(request, self.template_name, {'error': 'Passwords do not match'})

        # Create a new user
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)  # Log the user in

        return redirect('home')  # Redirect to the home page or any other desired page


class HomeView(TemplateView):
    template_name = 'home.html'