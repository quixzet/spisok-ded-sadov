from django.urls import path
from . import views

app_name = 'standoff2'

urlpatterns = [
    path('', views.kindergarten_list, name='kindergarten_list'),
    path('kindergartens/', views.kindergarten_list, name='kindergarten_list'),
    path('kindergartens/<int:pk>/', views.kindergarten_detail, name='kindergarten_detail'),
    path('teachers/', views.teacher_list, name='teacher_list'),
     path('teachers/create/', views.teacher_create, name='teacher_create'),
]