from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('view-exam/<int:exam_id>/', views.view_exam, name='view_exam'),
    path('delete-exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('students/', views.list_students, name='list_students'),
    path('students/<int:student_id>/results/', views.student_results, name='student_results'),
]


