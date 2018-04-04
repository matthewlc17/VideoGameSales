from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template

# Create your views here.
def landingpage(request):

    context = {}

    return render(request, 'homepage/landingpage.html', context)
