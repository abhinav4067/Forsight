from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
    path('toggle-replied/', views.toggle_replied, name='toggle_replied'),  # ✅
    path('our_team/', views.our_team, name='our_team'),
    path('learning_modules/', views.learning_modules, name='learning_modules'),
    path('register/', views.student_registration_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_out/', views.logout_user, name='log_out'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('export/', views.export_students_csv, name='export_csv'),
    path('export-pdf/', views.export_students_pdf, name='export_pdf'),
    path('admin_reg/', views.register_user, name='admin_reg'),
    path('admin_login/', views.login_user, name='admin_login'),
    path('admin_forget/', views.admin_forget, name='admin_forget'),
    path('export_enquiries_csv/', views.export_enquiries_csv, name='export_enquiries_csv'),
    path('export_enquiries_pdf/', views.export_enquiries_pdf, name='export_enquiries_pdf'),



    path('add_post/', views.post_create, name='post_create'),
    path('edit_post/<int:pk>/', views.post_edit, name='post_edit'),
    path('delete_post/<int:pk>/', views.post_delete, name='post_delete'),
    path('admission/', views.admission, name='admission'),
    path('students/details/<int:student_id>/', views.student_details_json, name='student_details_json'),


]
