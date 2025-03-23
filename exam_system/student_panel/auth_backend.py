from django.contrib.auth.backends import BaseBackend
from student_panel.models import Student  # Import Student Model

class StudentAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = Student.objects.get(registration_number=username)
            if student.check_password(password):  # Verify password
                return student
        except Student.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
