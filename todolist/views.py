from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todolist/home.html')


def user_sign_up(request):
    if request.method == 'GET':
        return render(request, 'todolist/user_sign_up.html', {'form': UserCreationForm()})
    else:
        if len(str(request.POST['password1'])) > 8:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    new_user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    new_user.save()
                    login(request, new_user)
                    return redirect('to_dos')

                except IntegrityError:
                    return render(request, 'todolist/user_sign_up.html',
                                  {'form': UserCreationForm(), 'error': 'User Name '
                                                                        'already '
                                                                        'Taken! Try '
                                                                        'another '
                                                                        'one!'})

            else:
                return render(request, 'todolist/user_sign_up.html',
                              {'form': UserCreationForm(), 'error': 'Passwords did '
                                                                    'not match!'})
        else:
            return render(request, 'todolist/user_sign_up.html', {'form': UserCreationForm(), 'error': 'Password '
                                                                                                       'needs to be '
                                                                                                       'at least 8 '
                                                                                                       'characters '
                                                                                                       'long'})


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def user_login(request):
    if request.method == 'GET':
        return render(request, 'todolist/user_login.html', {'form': AuthenticationForm()})
    else:
        logged_user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if logged_user is None:
            return render(request, 'todolist/user_login.html', {'form': AuthenticationForm(), 'error': 'Username or '
                                                                                                       'Password did '
                                                                                                       'not match!'})
        else:
            login(request, logged_user)
            return redirect('to_dos')


@login_required
def to_dos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todolist/to_dos.html', {'todos': todos})


@login_required
def completed_to_dos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todolist/completed_to_dos.html', {'todos': todos})


@login_required
def create_to_dos(request):
    if request.method == 'GET':
        return render(request, 'todolist/create_to_dos.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('to_dos')
        except ValueError:
            return render(request, 'todolist/create_to_dos.html', {'form': TodoForm(), 'error': 'Title can not be '
                                                                                                'more than 100 '
                                                                                                'characters'})


@login_required
def view_to_do(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todolist/view_to_do.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('to_dos')
        except ValueError:
            return render(request, 'todolist/view_to_do.html', {'todo': todo, 'form': form, 'error': 'Error while '
                                                                                                     'parsing data!'})


@login_required
def complete_to_do(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('to_dos')


@login_required
def delete_to_do(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('to_dos')
