from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .forms import InternshipForm
from .models import Internship

def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('login')   
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login')
        else:
            login(request, user)
            return redirect('main')
    return render(request, 'login.html')

def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('signup')
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        messages.success(request, "Account created successfully!")
        return redirect('login')
    return render(request, 'signup.html')


@require_POST
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def main_page(request):
    form_data = request.POST if request.method == 'POST' else None
    form = InternshipForm(form_data)
    if request.method == 'POST' and form.is_valid():
        internship = form.save(commit=False)
        internship.user = request.user
        internship.save()
        messages.success(request, 'Internship added to your tracker.')
        return redirect('main')

    internships = Internship.objects.filter(user=request.user)
    return render(request, 'main.html', {
        'internships': internships,
        'form': form,
        'show_add_modal': request.method == 'POST' and form.errors,
    })