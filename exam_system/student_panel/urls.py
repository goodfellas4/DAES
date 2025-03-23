from django.urls import path
from .views import student_signup,student_login,student_logout, student_home,start_exam,exam_results,submit_exam,verify_secret_key,written_exam_results

app_name = 'student_panel'  
urlpatterns = [
    path('signup/', student_signup, name='student_signup'),
    path('login/', student_login, name='student_login'),
    path('logout/', student_logout, name='student_logout'),
    path('home/', student_home, name='student_home'),
    path('start-exam/<int:exam_id>/', start_exam, name='start_exam'),
    path('results/', written_exam_results, name='written_exam_results'),
    path('submit-exam/<int:exam_id>/',submit_exam, name='submit_exam'),
    path("verify_secret_key/", verify_secret_key, name="verify_secret_key"),
    path('exam/<int:exam_id>/results/', exam_results, name='exam_results'),
    
]
