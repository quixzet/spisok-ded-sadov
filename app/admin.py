from django.contrib import admin
from django.db.models import Avg, Count
from .models import (
    Child, Teacher, Kindergarten, Group, 
    Enrollment, Review, KindergartenTeacher,
    KindergartenImage
)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'parent_contact')
    list_filter = ('birth_date',)
    search_fields = ('first_name', 'last_name', 'parent_contact')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'birth_date'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'qualification', 'experience_years')
    list_filter = ('qualification', 'experience_years')
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name', 'first_name')


class KindergartenImageInline(admin.TabularInline):
    model = KindergartenImage
    extra = 1
    fields = ['image', 'caption', 'order']
    classes = ['collapse']


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1
    show_change_link = True
    classes = ['collapse']


class KindergartenTeacherInline(admin.TabularInline):
    model = KindergartenTeacher
    extra = 1
    show_change_link = True
    classes = ['collapse']
    autocomplete_fields = ['teacher']


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('parent_name', 'rating', 'comment')
    classes = ['collapse']


@admin.register(Kindergarten)
class KindergartenAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'capacity', 'established_at', 
                    'is_recommended', 'average_rating_display', 'groups_display', 'teachers_display')
    list_filter = ('established_at', 'capacity', 'is_recommended')
    search_fields = ('name', 'address', 'phone', 'description')
    ordering = ('name',)
    date_hierarchy = 'established_at'
    readonly_fields = ('average_rating_display', 'groups_display', 'teachers_display')
    list_editable = ('is_recommended',)
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['name', 'address', 'phone', 'description']
        }),
        ('Характеристики', {
            'fields': ['capacity', 'established_at', 'is_recommended', 'features']
        }),
        ('Статистика', {
            'fields': ['average_rating_display', 'groups_display', 'teachers_display'],
            'classes': ['collapse']
        }),
    ]
    
    inlines = [KindergartenImageInline, GroupInline, KindergartenTeacherInline, ReviewInline]
    
    def average_rating_display(self, obj):
        return f"{obj.average_rating:.1f}"
    average_rating_display.short_description = 'Средний рейтинг'
    
    def groups_display(self, obj):
        return obj.group_set.count()
    groups_display.short_description = 'Количество групп'
    
    def teachers_display(self, obj):
        return obj.kindergartenteacher_set.count()
    teachers_display.short_description = 'Количество воспитателей'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Используем другие имена для аннотаций, чтобы не конфликтовать с свойствами
        qs = qs.annotate(
            rating_avg=Avg('review__rating'),
            groups_cnt=Count('group', distinct=True),
            teachers_cnt=Count('kindergartenteacher', distinct=True)
        )
        return qs


@admin.register(KindergartenImage)
class KindergartenImageAdmin(admin.ModelAdmin):
    list_display = ('kindergarten', 'image_preview', 'caption', 'order', 'created_at')
    list_filter = ('kindergarten', 'created_at')
    search_fields = ('kindergarten__name', 'caption')
    ordering = ('kindergarten', 'order')
    list_editable = ('order',)
    
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return f'<img src="{obj.image.url}" style="max-height: 50px;" />'
        return "Нет фото"
    image_preview.allow_tags = True
    image_preview.short_description = 'Превью'


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    show_change_link = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'kindergarten', 'age_range', 'max_capacity', 'current_enrollment')
    list_filter = ('kindergarten', 'age_range')
    search_fields = ('name', 'age_range', 'kindergarten__name')
    ordering = ('kindergarten', 'name')
    inlines = [EnrollmentInline]
    
    def current_enrollment(self, obj):
        return f"{obj.enrollment_set.count()}/{obj.max_capacity}"
    current_enrollment.short_description = 'Заполненность'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'group', 'enrollment_date', 'status')
    list_filter = ('enrollment_date', 'status', 'group__kindergarten')
    search_fields = ('child__first_name', 'child__last_name', 'group__name')
    ordering = ('-enrollment_date',)
    date_hierarchy = 'enrollment_date'
    raw_id_fields = ('child', 'group')
    list_editable = ('status',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('kindergarten', 'parent_name', 'rating', 'stars_display', 'comment_preview', 'created_at')
    list_filter = ('rating', 'kindergarten', 'created_at')
    search_fields = ('parent_name', 'comment', 'kindergarten__name')
    ordering = ('-created_at', '-rating')
    raw_id_fields = ('kindergarten',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['kindergarten', 'parent_name', 'parent_email', 'parent_phone']
        }),
        ('Отзыв', {
            'fields': ['rating', 'comment']
        }),
        ('Даты', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '-'
    comment_preview.short_description = 'Комментарий (превью)'
    
    def stars_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)
    stars_display.short_description = 'Рейтинг'


@admin.register(KindergartenTeacher)
class KindergartenTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'kindergarten', 'role', 'years_at_kindergarten')
    list_filter = ('kindergarten', 'role')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'kindergarten__name')
    ordering = ('kindergarten', 'teacher')
    raw_id_fields = ('teacher', 'kindergarten')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher', 'kindergarten')