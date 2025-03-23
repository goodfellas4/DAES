from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import json
import os

from .forms import AdminLoginForm
from .models import Exam
from student_panel.models import Student, StudentExam, StudentAnswer

# Admin Login View
def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Log out any existing session to avoid conflicts
            if request.user.is_authenticated:
                logout(request)

            # Authenticate admin user
            admin_user = authenticate(request, username=username, password=password)
            if admin_user and admin_user.is_staff:  # Check if the user is admin
                login(request, admin_user)
                messages.success(request, "Admin login successful!")
                return redirect('admin_dashboard')  # Redirect to dashboard
            else:
                messages.error(request, "Invalid admin credentials.")
    else:
        form = AdminLoginForm()

    return render(request, 'admin_panel/login.html', {'form': form})

# Admin Dashboard View to upload exams
@login_required
def admin_dashboard(request):
    exams = Exam.objects.all()  # Fetch all exams
    if request.method == 'POST' and request.FILES.get('json_file'):
        exam_file = request.FILES['json_file']
        fs = FileSystemStorage()

        # Save file and get file path
        filename = fs.save(exam_file.name, exam_file)
        full_file_path = os.path.join(fs.location, filename)

        try:
            # Load and parse JSON file
            with open(full_file_path, 'r') as file:
                data = json.load(file)
                exam_title = data.get('exam_title', 'Untitled Exam')

                # Create and save exam
                exam = Exam.objects.create(title=exam_title, json_file=exam_file)
                exam.save()

                # Create questions from JSON data
                for question_data in data.get('questions', []):
                    question_text = question_data.get('question_text', '')
                    ideal_answer = question_data.get('ideal_answer', '')
                    exam.questions.create(question_text=question_text, ideal_answer=ideal_answer)
            
            messages.success(request, "Exam uploaded successfully!")
        except Exception as e:
            messages.error(request, f"Error while processing the file: {e}")

        return redirect('admin_dashboard')

    return render(request, 'admin_panel/admin_dashboard.html', {'exams': exams})

# View to display details of a specific exam
@login_required
def view_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    return render(request, 'admin_panel/view_exam.html', {'exam': exam})

# Delete an exam from the system
@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    exam.delete()  # Delete the exam
    messages.success(request, "Exam deleted successfully!")
    return redirect('admin_dashboard')

# Admin Logout View
@login_required
def logout_view(request):
    logout(request)  # Log out the admin user
    return redirect('admin_login')

# List all students
@login_required
def list_students(request):
    students = Student.objects.all()
    return render(request, 'admin_panel/list_students.html', {'students': students})

# View results of a specific student
@login_required
def student_results(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    attempted_exams = StudentExam.objects.filter(student=student, is_completed=True)

    exam_results = []
    for exam in attempted_exams:
        answers = StudentAnswer.objects.filter(student=student, question__exam=exam.exam)
        total_score = sum(answer.score for answer in answers)  # Calculate total score for this exam
        exam_results.append({
            'exam': exam.exam,
            'total_score': total_score,
            'answers': answers
        })

    return render(request, 'admin_panel/student_results.html', {'student': student, 'exam_results': exam_results})


