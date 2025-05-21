from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.utils.dateparse import parse_date
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        user = CustomUser.objects.create_user(username=username, email=email, password=password, phone=phone)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')
    return render(request, 'tasks/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            response = redirect('dashboard')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            return response
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('access_token')
    return response

@login_required
def dashboard(request):
    user = request.user
    if user.role=='admin':
        users=CustomUser.objects.filter(role ='user')
        return render(request,'tasks/admin_user_list.html',{'users':users})
        
    else:
        tasks = Task.objects.filter(user=user).order_by('due_date')
        return render(request, 'tasks/dashboard.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        start_date = request.POST['start_date']
        due_date = request.POST['due_date']

        Task.objects.create(
            user=request.user,
            name=name,
            description=description,
            start_date=parse_date(start_date),
            due_date=parse_date(due_date),
            is_completed=False
        )
        return redirect('dashboard')

    return render(request, 'tasks/add_task.html')

@login_required
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if task.user != request.user and request.user.role != 'admin':
            return redirect('dashboard')
    except Task.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.start_date = parse_date(request.POST['start_date'])
        task.due_date = parse_date(request.POST['due_date'])
        task.save()
        if request.user.role == 'admin':
            return redirect('admin_view_tasks', user_id=task.user.id)
        else:
            return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if task.user != request.user and request.user.role != 'admin':
            return redirect('dashboard')
        user_id = task.user.id
        task.delete()
    except Task.DoesNotExist:
        pass

    if request.user.role == 'admin':
        return redirect('admin_view_tasks', user_id=user_id)
    else:
        return redirect('dashboard')


@login_required
def mark_done(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.is_completed = True
        task.save()
    except Task.DoesNotExist:
        pass
    return redirect('dashboard')

@login_required
def admin_user_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    users = CustomUser.objects.filter(role='user')
    return render(request, 'tasks/admin_user_list.html', {'users': users})

@login_required
def admin_view_tasks(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')
    try:
        user = CustomUser.objects.get(id=user_id, role='user')
    except CustomUser.DoesNotExist:
        return redirect('admin_user_list')
    tasks = Task.objects.filter(user=user)
    return render(request, 'tasks/admin_view_tasks.html', {'user_obj': user, 'tasks': tasks})

@login_required
def admin_edit_task(request, task_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']
        task.save()
        return redirect('admin_view_tasks', user_id=task.user.id)

    return render(request, 'tasks/admin_edit_task.html', {'task': task})

@login_required
def admin_delete_task(request, task_id):
    if request.user.role != 'admin':
        return redirect('dashboard')
    task = get_object_or_404(Task, id=task_id)
    user_id = task.user.id
    task.delete()
    return redirect('admin_view_tasks', user_id=user_id)

@login_required
def admin_delete_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')
    try:
        user = CustomUser.objects.get(id=user_id, role='user')
        user.delete()
    except CustomUser.DoesNotExist:
        pass
    return redirect('admin_user_list')




