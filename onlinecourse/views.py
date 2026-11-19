from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Lesson, Question, Choice, Submission

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})

@login_required
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    questions = lesson.questions.prefetch_related("choices")
    if request.method != "POST":
        return redirect("course_details", course_id=lesson.course_id)
    score = 0
    answers = {}
    question_list = list(questions)
    for question in question_list:
        selected_id = request.POST.get(f"question_{question.id}")
        answers[str(question.id)] = selected_id or ""
        if selected_id and question.choices.filter(pk=selected_id, is_correct=True).exists():
            score += 1
    submission = Submission.objects.create(
        user=request.user, lesson=lesson, answers=answers,
        score=score, total_questions=len(question_list),
    )
    return redirect("show_exam_result", submission_id=submission.id)

@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    questions = submission.lesson.questions.prefetch_related("choices")
    results = []
    for question in questions:
        selected_id = submission.answers.get(str(question.id))
        selected = question.choices.filter(pk=selected_id).first() if selected_id else None
        correct = question.choices.filter(is_correct=True).first()
        results.append({"question": question, "selected": selected, "correct": correct,
                        "is_correct": bool(selected and selected.is_correct)})
    percentage = round((submission.score / submission.total_questions) * 100) if submission.total_questions else 0
    return render(request, "onlinecourse/exam_result.html", {
        "submission": submission, "results": results, "percentage": percentage,
    })
