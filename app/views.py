from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Kindergarten, Teacher, Review


def kindergarten_list(request):
    # Получаем все детские сады с префетчингом
    kindergartens = Kindergarten.objects.all().prefetch_related(
        'group_set', 
        'kindergartenteacher_set', 
        'review_set'
    )
    
    # Получаем параметры фильтрации из GET-запроса
    district = request.GET.get('district')
    age_group = request.GET.get('age')
    specialization = request.GET.get('specialization')
    
    # Применяем фильтры если они есть
    if district and district != 'Все районы':
        kindergartens = kindergartens.filter(district=district)
    
    if age_group and age_group != 'Любой возраст':
        # Предполагаем, что в модели есть поля min_age и max_age
        # Если их нет, добавьте в модель Kindergarten:
        # min_age = models.IntegerField(default=1)
        # max_age = models.IntegerField(default=6)
        if age_group == '1-2 года':
            kindergartens = kindergartens.filter(min_age__lte=2, max_age__gte=1)
        elif age_group == '3-4 года':
            kindergartens = kindergartens.filter(min_age__lte=4, max_age__gte=3)
        elif age_group == '5-6 лет':
            kindergartens = kindergartens.filter(min_age__lte=6, max_age__gte=5)
    
    if specialization and specialization != 'Любая':
        # Для специализации нужно добавить поле в модель
        # specialization = models.CharField(max_length=100, blank=True)
        kindergartens = kindergartens.filter(specialization__icontains=specialization)
    
    return render(request, 'kindergarten_list.html', {
        'kindergartens': kindergartens,
        'current_page': 'kindergartens',
        'selected_district': district or 'Все районы',
        'selected_age': age_group or 'Любой возраст',
        'selected_specialization': specialization or 'Любая'
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
        # Фильтруем учителей по детскому саду
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