from django.conf import settings
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "course")
    def __str__(self):
        return f"{self.user} - {self.course}"

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="questions", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.choice_text

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} - {self.lesson} ({self.score}/{self.total_questions})"

class LessonCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user", "lesson")
    def __str__(self):
        return f"{self.user} completed {self.lesson}"
