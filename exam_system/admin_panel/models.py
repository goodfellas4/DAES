

# Create your models here.
from django.db import models

# Create Exam Model
class Exam(models.Model):
    title = models.CharField(max_length=200)  # Title of the exam
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time when exam is created
    json_file = models.FileField(upload_to='exam_files/')  # JSON file containing questions and answers

    def __str__(self):
        return self.title


# Create Question Model
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')  # Link to Exam
    question_text = models.TextField()  # Text of the question
    ideal_answer = models.TextField()  # Ideal answer for evaluation

    def __str__(self):
        return f"Question {self.id} for {self.exam.title}"
