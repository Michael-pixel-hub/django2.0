from django.contrib import admin
from mainapp import models
from django.utils.translation import gettext_lazy as _


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'preambule', 'body']


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_course_name', 'num', 'title']
    ordering = ['-title']
    list_per_page = 5
    list_filter = ['course', 'created', 'deleted']
    actions = ["mark_deleted"]

    def get_course_name(self, obj):
        return obj.course.name

    get_course_name.short_description = _('Course')

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _("Mark deleted")


@admin.register(models.Courses)
class CoursesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CourseFeedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ['title', 'preambule', 'body']