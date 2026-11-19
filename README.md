# Django Online Course Final Project

A Django application for managing online courses, lessons, mock exams, questions, choices, and student submissions.

## Features
- Course and lesson pages
- Django admin configuration for courses, lessons, questions, choices, and submissions
- Mock exam submission and result views
- Bootstrap-based course details template

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and visit /admin/ for administration.

This is a self-contained educational Django implementation. Configure sample course and exam data through the Django admin before attempting an exam.