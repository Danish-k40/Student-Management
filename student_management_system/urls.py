
from os import name
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from student_management_system import settings
from app import views,adminView,StudentViews


urlpatterns = [
    path('signup_admin',views.signup_admin,name="signup_admin"),
    path('signup_student',views.signup_student,name="signup_student"),
    path('signup_staff',views.signup_staff,name="signup_staff"),
    path('do_admin_signup',views.do_admin_signup,name="do_admin_signup"),
    path('do_staff_signup',views.do_staff_signup,name="do_staff_signup"),
    path('do_signup_student',views.do_signup_student,name="do_signup_student"),
    path('',views.ShowLoginPage,name="show_login"),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),



    path('admin/', admin.site.urls),
    # path('', views.demo, name="demo"),
    path('admin_home', adminView.admin_home, name='admin_home'),
    path('add_student', adminView.add_student, name='add_student'),
    path('add_student_save', adminView.add_student_save, name='add_student_save'),
    path('check_email_exist', adminView.check_email_exist,name="check_email_exist"),
    path('check_username_exist', adminView.check_username_exist,name="check_username_exist"),
    path('manage_session', adminView.manage_session,name="manage_session"),
    path('add_session_save', adminView.add_session_save,name="add_session_save"),
    path('manage_student', adminView.manage_student,name="manage_student"),
    path('search', adminView.Student_searching, name='search'),
    path('student_feedback_message', adminView.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replied', adminView.student_feedback_message_replied,name="student_feedback_message_replied"),
    path('admin_send_notification_student', adminView.admin_send_notification_student,name="admin_send_notification_student"),
    path('send_student_notification', adminView.send_student_notification,name="send_student_notification"),
    
    
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_all_notification',StudentViews.student_all_notification,name="student_all_notification"),




]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
