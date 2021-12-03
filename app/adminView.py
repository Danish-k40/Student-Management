from django import forms
from django.http.response import HttpResponse
from django.shortcuts import render
from app.models import CustomUser, SessionYearModel, Admin, Students, NotificationStudent, FeedBackStudent
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from app.forms import EditStudentForm
from django.db.models import Q
import json
import requests
from django.contrib.auth.decorators import login_required


from django.core.files.storage import FileSystemStorage
# from app.forms import AddStudentForm


@login_required(login_url='/doLogin')
def admin_home(request):

    student_count1=Students.objects.all().count()
    students_all=Students.objects.all()
    student_name_list=[]
    for student in students_all:
        student_name_list.append(student.admin.username)
    return render(request, "Admin_Templates/admin_home.html", {"student_count":student_count1,"student_name_list":student_name_list,})
def add_student(request):
    return render(request,"Admin_Templates/add_student_template.html")

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        roll_number = request.POST['roll_number']
        collage = request.POST['collage']
        context = {
            'fieldValues': request.POST
        }
        try:
            if not CustomUser.objects.filter(email=email).exists():
                if not CustomUser.objects.filter(username=username).exists():

                    if not Students.objects.filter(phone=phone).exists():
                            if len(password) < 6:
                                messages.error(request, "password too short")
                                return render(request, 'Admin_Templates/add_student_template.html', context)
                            user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
                                    # send email for activation
                            user.students.collage=collage
                            user.students.phone=phone
                            user.students.roll_number=roll_number
                            user.save()
                            messages.success(request, "Account successfully created")
                            return HttpResponseRedirect(reverse("add_student"))
                            
                                
                    else:
                        messages.error(request,"This phone number already used!")
                        return HttpResponseRedirect(reverse("add_student"))
                else:
                    messages.error(request,"This user name already used!")
                    return HttpResponseRedirect(reverse("add_student"))
            else:
                messages.error(request,"This email already used!")
                return HttpResponseRedirect(reverse("add_student"))


        except:
                messages.error(request,"Somthing wrong!")
                return HttpResponseRedirect(reverse("add_student"))
def manage_student(request):
    students=Students.objects.all()
    return render(request,"Admin_Templates/manage_student_template.html",{"students":students})

def Student_searching(request):
    stud = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        stud= CustomUser.objects.all().filter(Q(username__contains=query))

    return render(request, 'Admin_Templates/search.html', {'qr': query, 'st': stud})


def manage_session(request):
    return render(request,"Admin_Templates/manage_session_template.html")

def add_session_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year=request.POST.get("session_start")
        session_end_year=request.POST.get("session_end")

        try:
            sessionyear=SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

def student_feedback_message(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"Admin_Templates/student_feedback_template.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def admin_send_notification_student(request):
    students=Students.objects.all()
    return render(request,"Admin_Templates/student_notification.html",{"students":students})

@csrf_exempt
def send_student_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    student=Students.objects.get(admin=id)
    token=student.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
            "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStudent(student_id=student,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")


@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
