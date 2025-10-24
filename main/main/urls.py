"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from standoff2 import views  # добавьте этот импорт

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.kindergarten_list, name='kindergarten_list'),
    path('kindergartens/<int:pk>', views.kindergarten_list, name='kindergarten_detail'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('reviews/', views.review_list, name='review_list'),
]