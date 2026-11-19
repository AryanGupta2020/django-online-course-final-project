from django.contrib import admin
from .models import (
    Course, Lesson, Enrollment, Question, Choice, Submission, LessonCompletion,
)

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson")
    inlines = [ChoiceInline]

admin.site.register(Enrollment)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(LessonCompletion)
