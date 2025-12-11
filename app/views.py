# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Kindergarten, Teacher, Review
from .forms import ReviewForm


def kindergarten_list(request):
    kindergartens = Kindergarten.objects.annotate(
        avg_rating_value=Avg('review__rating'),
        groups_count_value=Count('group', distinct=True),
        teachers_count_value=Count('kindergartenteacher', distinct=True),
        reviews_count=Count('review', distinct=True)
    )
    
    search_query = request.GET.get('search', '')
    if search_query:
        kindergartens = kindergartens.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(features__icontains=search_query)
        )
    
    sort_by = request.GET.get('sort', '')
    if sort_by == 'rating':
        kindergartens = kindergartens.order_by('-avg_rating_value')
    elif sort_by == 'name':
        kindergartens = kindergartens.order_by('name')
    elif sort_by == 'capacity':
        kindergartens = kindergartens.order_by('-capacity')
    elif sort_by == 'recommended':
        kindergartens = kindergartens.order_by('-is_recommended', 'name')
    else:
        kindergartens = kindergartens.order_by('-is_recommended', '-avg_rating_value')
    
    context = {
        'kindergartens': kindergartens,
        'search_query': search_query,
    }
    return render(request, 'kindergarten_list.html', context)


def kindergarten_detail(request, pk):
    kindergarten = get_object_or_404(Kindergarten.objects.prefetch_related(
        'group_set', 'group_set__enrollment_set__child',
        'kindergartenteacher_set__teacher', 'review_set'
    ), pk=pk)
    
    reviews = kindergarten.review_set.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST' and 'add_review' in request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.kindergarten = kindergarten
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен и будет опубликован после модерации.')
            return redirect('kindergarten_detail', pk=kindergarten.pk)
    else:
        form = ReviewForm(initial={'kindergarten': kindergarten, 'rating': 5})
    
    context = {
        'kindergarten': kindergarten,
        'avg_rating': avg_rating,
        'reviews_count': reviews.count(),
        'form': form,
    }
    return render(request, 'kindergarten_detail.html', context)


def add_review(request, kindergarten_id):
    kindergarten = get_object_or_404(Kindergarten, pk=kindergarten_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.kindergarten = kindergarten
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
            return redirect('kindergarten_detail', pk=kindergarten.pk)
    else:
        form = ReviewForm(initial={'kindergarten': kindergarten, 'rating': 5})
    
    context = {
        'kindergarten': kindergarten,
        'form': form,
    }
    return render(request, 'add_review.html', context)


def review_list(request):
    reviews = Review.objects.select_related('kindergarten').all().order_by('-created_at')
    
    kindergarten_id = request.GET.get('kindergarten')
    if kindergarten_id:
        reviews = reviews.filter(kindergarten_id=kindergarten_id)
    
    kindergartens = Kindergarten.objects.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    if request.method == 'POST' and 'add_review' in request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('review_list')
    else:
        form = ReviewForm()
    
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'reviews': page_obj,
        'kindergartens': kindergartens,
        'avg_rating': avg_rating,
        'reviews_count': reviews.count(),
        'is_paginated': paginator.num_pages > 1,
        'form': form,
    }
    return render(request, 'review_list.html', context)


def teacher_list(request):
    teachers = Teacher.objects.all()
    
    kindergarten_id = request.GET.get('kindergarten')
    if kindergarten_id:
        teachers = teachers.filter(kindergartenteacher__kindergarten_id=kindergarten_id)
    
    kindergartens = Kindergarten.objects.all()
    
    paginator = Paginator(teachers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'teachers': page_obj,
        'kindergartens': kindergartens,
        'is_paginated': paginator.num_pages > 1,
    }
    return render(request, 'teacher_list.html', context)