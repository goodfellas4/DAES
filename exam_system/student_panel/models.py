from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from admin_panel.models import Question, Exam

# Custom Manager for Student Model
class StudentManager(BaseUserManager):
    def create_user(self, registration_number, name, course, password=None):
        if not registration_number:
            raise ValueError("Students must have a registration number")
        if not name:
            raise ValueError("Students must have a name")
        if not course:
            raise ValueError("Students must have a course")

        student = self.model(
            registration_number=registration_number, name=name, course=course
        )
        student.set_password(password)
        student.save(using=self._db)
        return student

class Student(AbstractBaseUser):
    registration_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = StudentManager()

    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['name', 'course']

    def __str__(self):
        return f"{self.name} ({self.registration_number})"

class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.TextField()
    score = models.FloatField(default=0)

    class Meta:
        unique_together = ('student', 'question')  # Ensure one answer per student per question

    def __str__(self):
        return f"Answer by {self.student.name} for {self.question.id} - Score: {self.score}"
    
class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  # Store exam start time
    is_completed = models.BooleanField(default=False)  # Track if the student has finished

    def __str__(self):
        return f"{self.student.name} - {self.exam.title}"
