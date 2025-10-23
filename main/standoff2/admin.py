from django.contrib import admin
from .models import (
    Child, Teacher, Kindergarten, 
    Group, Enrollment, Review, KindergartenTeacher
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
    list_display = ('first_name', 'last_name', 'phone_number', 'qualification')
    list_filter = ('qualification',)
    search_fields = ('first_name', 'last_name', 'phone_number')
    ordering = ('last_name', 'first_name')


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1
    show_change_link = True


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('parent_name', 'rating', 'comment')


class KindergartenTeacherInline(admin.TabularInline):
    model = KindergartenTeacher
    extra = 1
    show_change_link = True


@admin.register(Kindergarten)
class KindergartenAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'capacity', 'established_at', 'phone')
    list_filter = ('established_at', 'capacity')
    search_fields = ('name', 'address', 'phone')
    ordering = ('name',)
    date_hierarchy = 'established_at'
    inlines = [GroupInline, ReviewInline, KindergartenTeacherInline]


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    show_change_link = True


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'kindergarten', 'age_range')
    list_filter = ('kindergarten', 'age_range')
    search_fields = ('name', 'age_range')
    ordering = ('kindergarten', 'name')
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('child', 'group', 'enrollment_date', 'status')
    list_filter = ('enrollment_date', 'status', 'group__kindergarten')
    search_fields = ('child__first_name', 'child__last_name', 'group__name')
    ordering = ('-enrollment_date',)
    date_hierarchy = 'enrollment_date'
    raw_id_fields = ('child', 'group')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('kindergarten', 'parent_name', 'rating', 'comment_preview')
    list_filter = ('rating', 'kindergarten')
    search_fields = ('parent_name', 'comment', 'kindergarten__name')
    ordering = ('-rating', 'kindergarten')
    raw_id_fields = ('kindergarten',)
    
    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '-'
    comment_preview.short_description = 'Комментарий (превью)'


@admin.register(KindergartenTeacher)
class KindergartenTeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'kindergarten')
    list_filter = ('kindergarten',)
    search_fields = ('teacher__first_name', 'teacher__last_name', 'kindergarten__name')
    ordering = ('kindergarten', 'teacher')
    raw_id_fields = ('teacher', 'kindergarten')