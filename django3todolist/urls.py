"""django3todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todolist import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Authentication
    path('signup/', views.user_sign_up, name='user_sign_up'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),

    # ToDo's
    path('todos/', views.to_dos, name='to_dos'),
    path('create/', views.create_to_dos, name='create_to_dos'),
    path('completed/', views.completed_to_dos, name='completed_to_dos'),
    path('todos/<int:todo_pk>', views.view_to_do, name='view_to_do'),
    path('todos/<int:todo_pk>/complete', views.complete_to_do, name='complete_to_do'),
    path('todos/<int:todo_pk>/delete', views.delete_to_do, name='delete_to_do'),
]
