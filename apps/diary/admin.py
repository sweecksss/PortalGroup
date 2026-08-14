from django.contrib import admin
from .models import StudentProfile, Subject, Grade


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_class')
    list_filter = ('school_class',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'date_given', 'given_by')
    list_filter = ('subject', 'date_given')
    search_fields = ('student__user__username', 'student__user__last_name')
    autocomplete_fields = ('student', 'subject')

    def save_model(self, request, obj, form, change):
        if not obj.given_by_id:
            obj.given_by = request.user
        super().save_model(request, obj, form, change)
