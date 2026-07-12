from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect('index')
    
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/index.html', {'tasks': tasks})

@login_required
def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('index')

@login_required
def delete_task(request, task_id):
    Task.objects.filter(id=task_id, user=request.user).delete()
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/auth.html', {'form': form, 'title': 'Register', 'link': 'login', 'link_text': 'Already have an account? Log in'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/auth.html', {'form': form, 'title': 'Log In', 'link': 'register', 'link_text': 'Need an account? Register'})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')
