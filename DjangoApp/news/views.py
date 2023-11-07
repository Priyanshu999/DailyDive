from django.views.generic.edit import FormView
from .forms import CustomSignupForm
from django.views.generic import TemplateView
from django.contrib.auth import login
# from verify_email.email_handler import send_verification_email
# from django.shortcuts import render, re
# from django.views import View
# from django.contrib.auth.models import User

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = CustomSignupForm
    success_url = '/'  # Provide the URL name for the 'home' view

    def form_valid(self, form):
        # send_verification_email(self.request, form)
        # user = form.instance
        user = form.save()
        login(self.request, user)  # Log the user in
        return super().form_valid(form)
    

class HomeView(TemplateView):
    template_name = 'index.html'

