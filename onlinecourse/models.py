from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    STUDENT = "student"
    DEVELOPER = "developer"
    DATA_SCIENTIST = "data_scientist"
    DATABASE_ADMIN = "dba"

    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT)
    social_link = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username}, {self.occupation}"


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
    course = models.ForeignKey(
        Course, related_name="questions", on_delete=models.CASCADE,
        null=True, blank=True
    )
    question_text = models.CharField(max_length=500)
    content = models.CharField(max_length=500, blank=True)
    grade = models.IntegerField(default=50)

    def save(self, *args, **kwargs):
        if not self.content:
            self.content = self.question_text
        if not self.course_id and self.lesson_id:
            self.course = self.lesson.course
        super().save(*args, **kwargs)

    def is_get_score(self, selected_ids):
        selected_ids = [int(choice_id) for choice_id in selected_ids]
        all_answers = self.choices.filter(is_correct=True).count()
        selected_correct = self.choices.filter(
            is_correct=True, id__in=selected_ids
        ).count()
        selected_incorrect = self.choices.filter(
            is_correct=False, id__in=selected_ids
        ).count()
        return all_answers == selected_correct and selected_incorrect == 0

    def __str__(self):
        return self.content or self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, related_name="submissions", on_delete=models.CASCADE,
        null=True, blank=True
    )
    choices = models.ManyToManyField(Choice, related_name="submissions", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    answers = models.JSONField(default=dict, blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.pk} ({self.score}/{self.total_questions})"


class LessonCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user} completed {self.lesson}"
