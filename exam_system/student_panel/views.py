from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import json

from .models import StudentAnswer, Student, StudentExam
from admin_panel.models import Exam, Question
from .forms import StudentSignupForm, StudentLoginForm
from .evaluation import evaluate_answer

# ------------------------------
# Authentication Views
# ------------------------------

def student_signup(request):
    if request.method == "POST":
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])  # Encrypt password
            student.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('student_panel:student_login')
        messages.error(request, "Signup failed. Please check the form.")
    else:
        form = StudentSignupForm()
    return render(request, 'student_panel/signup.html', {'form': form})

def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            password = form.cleaned_data['password']
            
            if request.user.is_authenticated:
                logout(request)  # Logout any existing user session

            student = authenticate(request, username=registration_number, password=password)
            if student:
                login(request, student)
                messages.success(request, "Login successful!")
                return redirect('student_panel:student_home')
            messages.error(request, "Invalid registration number or password.")
    else:
        form = StudentLoginForm()
    return render(request, 'student_panel/login.html', {'form': form})

def student_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('student_panel:student_login')

# ------------------------------
# Student Dashboard
# ------------------------------

@login_required
def student_home(request):
    exams = Exam.objects.all()
    attempted_exams = StudentExam.objects.filter(student=request.user, is_completed=True).values_list('exam_id', flat=True)
    
    # Get student details
    student = request.user  # The logged-in student

    return render(request, 'student_panel/home.html', {
        'exams': exams,
        'attempted_exams': attempted_exams,
        'student': student  # Pass student details to the template
    })
# ------------------------------
# Exam Handling
# ------------------------------

@login_required
def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    student_exam, created = StudentExam.objects.get_or_create(student=request.user, exam=exam)
    
    if created:
        student_exam.start_time = timezone.now()
        student_exam.save()

    current_question_index = request.session.get('current_question', 0)
    current_question = questions[current_question_index] if current_question_index < len(questions) else None

    if request.method == 'POST' and current_question:
        student_answer = request.POST.get('answer')
        if student_answer:
            existing_answer = StudentAnswer.objects.filter(student=request.user, question=current_question).first()
            if not existing_answer:
                scores = evaluate_answer(current_question.question_text, current_question.ideal_answer, student_answer)
                StudentAnswer.objects.create(student=request.user, question=current_question, response=student_answer, score=scores['scaled_score'])
        
        current_question_index += 1
        request.session['current_question'] = current_question_index
        
        if current_question_index < len(questions):
            return redirect('student_panel:start_exam', exam_id=exam.id)
        else:
            student_exam.is_completed = True
            student_exam.save()
            return redirect('student_panel:submit_exam', exam_id=exam.id)
    
    elapsed_time = (timezone.now() - student_exam.start_time).total_seconds()
    remaining_time = max(0, (30 * 60) - elapsed_time)

    return render(request, 'student_panel/exam.html', {
        'exam': exam,
        'current_question': current_question,
        'question_index': current_question_index + 1,
        'total_questions': len(questions),
        'remaining_time': int(remaining_time),
    })

@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    student_answers = StudentAnswer.objects.filter(student=request.user, question__in=questions)
    missing_answers = len(questions) - len(student_answers)

    student_exam = StudentExam.objects.get(student=request.user, exam=exam)
    student_exam.is_completed = True
    student_exam.save()

    if request.method == 'POST' or request.GET.get('auto_submit'):
        return redirect('student_panel:exam_results', exam_id=exam.id)

    return render(request, 'student_panel/submit_exam.html', {
        'exam': exam,
        'missing_answers': missing_answers,
        'total_questions': len(questions),
    })

# ------------------------------
# Exam Results
# ------------------------------

@login_required
def exam_results(request, exam_id):
    """View for detailed results of a specific exam."""
    exam = get_object_or_404(Exam, id=exam_id)
    student_answers = StudentAnswer.objects.filter(student=request.user, question__exam=exam)
    
    total_score = sum(answer.score for answer in student_answers)
    total_marks = exam.questions.count() * 10  # Assuming each question is worth 10 marks

    return render(request, 'student_panel/results.html', {
        'exam': exam,
        'student_answers': student_answers,
        'total_score': total_score,
        'total_marks': total_marks
    })


@login_required
def written_exam_results(request):
    """View for listing all completed exams of a student."""
    student_exams = StudentExam.objects.filter(student=request.user, is_completed=True)

    return render(request, 'student_panel/written_exam_results.html', {'student_exams': student_exams})

# ------------------------------
# Secret Key Verification
# ------------------------------

  # To allow POST requests from the frontend without CSRF token
def verify_secret_key(request):
    if request.method == "POST":
        data = json.loads(request.body)
        exam_id = data.get('exam_id')
        secret_key = data.get('secret_key')
        
        student = request.user
        is_valid = student.key == secret_key
        
        return JsonResponse({"valid": is_valid})
    
