from django.shortcuts import render, get_object_or_404
from .models import Kindergarten, Teacher, Review

def kindergarten_list(request):
    kindergartens = Kindergarten.objects.all().prefetch_related(
        'group_set', 
        'kindergartenteacher_set', 
        'review_set'
    )
    return render(request, 'kindergarten_list.html', {
        'kindergartens': kindergartens,
        'current_page': 'kindergartens'
    })

def kindergarten_detail(request, pk):
    kindergarten = get_object_or_404(
        Kindergarten.objects.prefetch_related(
            'group_set__enrollment_set__child',
            'kindergartenteacher_set__teacher',
            'review_set'
        ), 
        pk=pk
    )
    return render(request, 'kindergarten_detail.html', {
        'kindergarten': kindergarten,
        'current_page': 'kindergartens'
    })

def teacher_list(request):
    teachers = Teacher.objects.prefetch_related('kindergartenteacher_set__kindergarten')
    kindergarten_id = request.GET.get('kindergarten')
    
    if kindergarten_id:
        teachers = teachers.filter(kindergartenteacher_set__kindergarten_id=kindergarten_id)
    
    return render(request, 'teacher_list.html', {
        'teachers': teachers,
        'current_page': 'teachers'
    })

def review_list(request):
    reviews = Review.objects.select_related('kindergarten').order_by('-id')
    kindergarten_id = request.GET.get('kindergarten')
    
    if kindergarten_id:
        reviews = reviews.filter(kindergarten_id=kindergarten_id)
    
    return render(request, 'review_list.html', {
        'reviews': reviews,
        'current_page': 'reviews'
    })