from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Choice, Enrollment, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


def extract_answers(request):
    selected_ids = []
    for key, value in request.POST.items():
        if key.startswith("choice") or key.startswith("question_"):
            try:
                selected_ids.append(int(value))
            except (TypeError, ValueError):
                continue
    return selected_ids


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
    )
    lesson = course.lessons.first()

    submission = Submission.objects.create(
        enrollment=enrollment,
        user=request.user,
        lesson=lesson,
    )

    selected_ids = extract_answers(request)
    selected_choices = Choice.objects.filter(id__in=selected_ids)
    submission.choices.set(selected_choices)

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission,
        pk=submission_id,
        enrollment__course=course,
    )
    selected_choices = submission.choices.all()

    questions = Question.objects.filter(
        Q(course=course) | Q(lesson__course=course)
    ).distinct()

    results = []
    score = 0
    total_score = 0
    correct_count = 0

    for question in questions:
        correct_choices = question.choices.filter(is_correct=True)
        question_selected = selected_choices.filter(question=question)
        selected_ids = list(question_selected.values_list("id", flat=True))
        is_correct = question.is_get_score(selected_ids)

        total_score += question.grade
        if is_correct:
            score += question.grade
            correct_count += 1

        results.append({
            "question": question,
            "selected": question_selected,
            "correct": correct_choices,
            "is_correct": is_correct,
        })

    total_questions = questions.count()
    percentage = round((score / total_score) * 100) if total_score else 0

    submission.score = correct_count
    submission.total_questions = total_questions
    submission.save(update_fields=["score", "total_questions"])

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        {
            "course": course,
            "submission": submission,
            "results": results,
            "choices": selected_choices,
            "grade": percentage,
            "score": correct_count,
            "total_questions": total_questions,
            "total_score": score,
            "max_score": total_score,
        },
    )
