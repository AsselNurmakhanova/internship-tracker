from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.http import require_POST, require_http_methods
from .forms import InternshipForm, UserProfileForm
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

    all_internships = Internship.objects.filter(user=request.user)
    internship_count = all_internships.count()
    search_query = request.GET.get('q', '').strip()
    internships = all_internships
    if search_query:
        internships = internships.filter(
            Q(company__icontains=search_query)
            | Q(role__icontains=search_query)
            | Q(status__icontains=search_query)
            | Q(notes__icontains=search_query)
        )

    context = {
        'internships': internships,
        'internship_count': internship_count,
        'search_query': search_query,
        'form': form,
        'show_add_modal': request.method == 'POST' and form.errors,
    }
    if request.headers.get('HX-Request') == 'true':
        return render(request, 'internship_rows.html', context)
    return render(request, 'main.html', context)


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def edit_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk, user=request.user)
    if request.method == 'GET':
        if request.GET.get('cancel'):
            return render(request, 'internship_row.html', {'internship': internship})
        form = InternshipForm(instance=internship, prefix=f'internship-{internship.pk}')
    else:
        form = InternshipForm(
            request.POST,
            instance=internship,
            prefix=f'internship-{internship.pk}',
        )
        if form.is_valid():
            form.save()
            return render(request, 'internship_row.html', {'internship': internship})

    return render(request, 'internship_edit_row.html', {
        'internship': internship,
        'form': form,
    })


@login_required(login_url='login')
@require_POST
def delete_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk, user=request.user)
    internship.delete()
    if request.headers.get('HX-Request') != 'true':
        messages.success(request, 'Internship deleted from your tracker.')
        return redirect('main')

    internships = Internship.objects.filter(user=request.user)
    search_query = request.POST.get('q', '').strip()
    if search_query:
        internships = internships.filter(
            Q(company__icontains=search_query)
            | Q(role__icontains=search_query)
            | Q(status__icontains=search_query)
            | Q(notes__icontains=search_query)
        )
    return render(request, 'internship_rows.html', {
        'internships': internships,
        'internship_count': Internship.objects.filter(user=request.user).count(),
        'search_query': search_query,
        'include_count': True,
    })


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'profile_display.html', {
                'profile_user': request.user,
                'profile_updated': True,
            })
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile_edit.html', {'form': form})