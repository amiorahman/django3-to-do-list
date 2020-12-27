from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login


def home(request):
    return render(request, 'todolist/home.html')


def user_sign_up(request):
    if request.method == 'GET':
        return render(request, 'todolist/user_sign_up.html', {'form': UserCreationForm()})
    else:
        if len(request.POST['password1']) > 8:
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


def to_dos(request):
    return render(request, 'todolist/to_dos.html')
