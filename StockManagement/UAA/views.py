from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group, Permission
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.db import transaction
import os
import PyPDF2
import string
from InventorySystem.models import UserDetail

from UAA.models import OtpCode
def searchUserSelected(request):
    try:
        index_number = request.POST.get('index_number')
        user_info = DefaultUsers.objects.filter(number=index_number).first()
        current_class = StudentClass.objects.filter(level = user_info.level)
        context = {'user_info':user_info, 'current_class':current_class}
        return render(request, 'UAA/register.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def updateStudent(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            file = request.FILES['file']
            phone_no = request.POST.get('phone_no')

            user_id = request.user.id
            user = User.objects.filter(id = user_id).first()
            student_info = UserDetail.objects.filter(user=user).first()
            student_info.phone_number = phone_no
            student_info.email = email
            student_info.photo = file
            student_info.save()
            messages.success(request,'Student is deleted successful')

            return redirect('userProfilePage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def changePassword(request):
    try:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user_id = request.user.id
                user = User.objects.filter(id = user_id).first()
                user.set_password(password1)
                return redirect('userProfilePage')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def foggotenPassword(request):
    user = request.user
    if request.method == "POST":
        email = request.POST.get('username')
        is_user_exists = User.objects.filter(email=email).exists()
        opt_generated = ''
        status = True
        if is_user_exists:
            user = User.objects.filter(email=email).first()
            opt_objs = OtpCode.objects.filter(user = request.user)
            if opt_objs.exists():
                opt_obj = opt_objs.first()
                if opt_obj.get_status == 'Valid':
                    opt_generated = opt_obj.code
                    status = True
                else:
                    status = False
            else:
                status = False
            if not status:
                opt = random.randint(100000,999999)
                opt_generated = 'E-' + str(opt)
                OtpCode.objects.create(code = opt_generated, user = user)
            header = 'Resset Password'
            message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(header, message, email_from, [email])
            return redirect(f'../opt_sent/{user.id}')
    return render(request, 'UAA/foggotpassword.html')

def resend_password(request, id):
    user = User.objects.filter(id=id).first()
    otp = OtpCode.objects.filter(user = user).first()
    opt_generated =otp.code
    header = 'Resset Password'
    message = f"dear {user.first_name},\n we are heard that you lost your password account. Don't worry you can reset your password by returning to your browser and use the following code.\n {opt_generated}"
    email_from = settings.EMAIL_HOST_USER
    email_to = otp.user.email
    send_mail(header, message, email_from, [email_to])
    return redirect(f'../opt_sent/{user.id}')

def opt_sent(request, id):
    if request.method == "POST":
        code = request.POST.get('code')
        user = User.objects.filter(id=id).first()
        opts = OtpCode.objects.filter(user = user, is_used=False)
        for opt in opts:
            if opt == code:
                if opt.get_status == 'Valid':
                    opt.is_used = True
                    opt.save()
                    return redirect(f'../setting_password/{user.id}')
                else:
                    messages.error(request,'Code used has been arleady expired')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request,'Incorrect code used')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/opt-sent.html', context)

def setting_password(request, id):
    if request.method == "POST":
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.filter(id=id).first()
            user.set_password(password1)
            messages.success(request,'Your password Account is reseted successfully')
            return redirect('')

        else:
            messages.error(request,'Two password must be the same')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.filter(id=id).first()
    context = {'user':user}
    return render(request, 'UAA/new-password.html')

@transaction.atomic
def registerPage(request):
    try:
        if request.method == "POST":
            index_number = request.POST.get('index_number')
            email = request.POST.get('email')
            bod = request.POST.get('bod')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_no = request.POST.get('phone_no')
            password = request.POST.get('password')
            gender = request.POST.get('gender')

            User.objects.create_user(username=email, email=email, password=password)
            user = User.objects.filter(email= email).first()
            user.last_name = last_name
            user.first_name 
            user.save()
            UserDetail.objects.create(name = first_name, phone_number = phone_no, gender = gender, user= user)
            role = Group.objects.get_or_create(name = 'Seller')
            user.groups.add(role)
            return redirect('loginPage')

        context = {}
        return render(request, 'UAA/register.html', context)
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def loginPage(request):
    try:
        if request.method == "POST":
            username = request.POST.get('email')
            password = request.POST.get('password')
            user =authenticate(username=username, password=password)
            if user:
                login(request, user)
                if user.is_active:
                    messages.success(request,'User is successful logged in')
                    return redirect('DashboardPage')
                elif user.is_superuser:
                    return redirect('admin')
                else:
                    messages.error(request,'Account is blocked')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request,'Incorrect username or password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'UAA/login.html')

def logoutPage(request):
    try:
        logout(request)
        return redirect('loginPage')
    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def manageroles(request):
    try:
        roles_dict= []
        Roles = Group.objects.all().order_by('id')
        for role in Roles:
            permisions = role.permissions.all()
            roles_dict.append({'role':role, 'permissions':permisions})

        context = {'roles_dict':roles_dict}
        return render(request,'UAA/manageroles.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def addroles(request):
    p = Group()
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            permission = [x.name for x in Permission.objects.all()]
            s_id = []
            p.name=name
            for x in permission:
                    s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
            p.save()
            messages.success(request,'Student is deleted successful')

            for s in s_id:
                p.permissions.add(Permission.objects.filter(id=s).first())
                p.save()
                messages.success(request,'Student is deleted successful')

            messages.success(request,'Role added successful')
            return redirect('/manageroles')

        except:
            messages.error(request,'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        permission = Permission.objects.all()
        context = {'permission':permission}
        return render(request, 'UAA/add-role.html', context)

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def RemoveRole(request, rid, pid):
    try:
        permission = Permission.objects.filter(id = pid).first()
        roles = Group.objects.filter(id = rid).first()
        roles.permissions.remove(permission)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def AssignUserRole(request, uid):
    user = User.objects.filter(id = uid).first()
    if request.method == 'POST':
        for j in user.groups.all():
            user.groups.remove(j)
        groups = [x.name for x in Group.objects.all()]

        s_id = []
        for x in groups:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        print(s_id)
        for s in s_id:
            user.groups.add(Group.objects.filter(id=s).first())
        messages.success(request,'roles are assigned to user successful')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def editroles(request,id):
    exclude_perm=[1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,37]
    p = Permission.objects.exclude(id__in=exclude_perm)
    r = Group.objects.filter(id=id)
    y=Group.objects.filter(id=id).first()
    if request.method == 'POST':
        name = request.POST.get('name')
        for j in Permission.objects.all():
            y.permissions.remove(j)
        permission = [x.name for x in Permission.objects.all()]

        s_id = []
        Group.objects.filter(id=id)
        for x in permission:
            s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        r=Group.objects.filter(id=id).update(name=name)

        for s in s_id:
            y.permissions.add(Permission.objects.get(id=s))
        messages.success(request,'permissions are added successful')
        return redirect('/manageroles')

    role = Group.objects.filter(id = id).first()
    permission = Permission.objects.all()
    context = {'permission':permission, 'role':role}
    return render(request, 'UAA/edit-role.html', context)

@login_required(login_url='/login')
def blockuser(request,id):
      try:
        u = User.objects.filter(id=id).filter(is_active='True').exists()
        if u:
            User.objects.filter(id=id).update(is_active='False')
            messages.success(request,'block successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            User.objects.filter(id=id).update(is_active='True')
            messages.success(request,'Activation successful')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      except:
       messages.error(request,'Something went Wrong')
       return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def deleteroles(request,id):
    g = Group.objects.filter(id=id).delete()
    messages.success(request,'Student is deleted successful')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def userProfilePage(request):
    return render(request, 'Admin/profile.html')

@login_required(login_url='/')
def DashboardPage(request):
    teacher_class = 0
    no_student = 0
    user =User.objects.filter(id = request.user.id).first()
    role_exist = user.groups.exists()
    if role_exist:
        role = user.groups.first().name
        if user.is_superuser:
            no_student = Student.objects.all().count()
        elif user.is_staff:
            teacher = Teacher.objects.filter(user = user)
            if teacher.exists():
                teacher_obj = teacher.first()
                teacher_class = teacher_obj.classSubject.all().count()
        elif Student.objects.filter(user= user).exists():
            student = Student.objects.filter(user= user).first()
            no_student = Student.objects.filter(classCurrent = student.classCurrent).count()
        context = {'role':role, 'teacher_class':teacher_class, 'no_student':no_student}
    context = {}
    return render(request, 'Admin/dashboard.html', context)

def Admision_statusPage(request):
    return render(request, 'Student/admission_status.html')

@login_required(login_url='/')
def studentList(request):
# try:
    student_list = []
    teachers_list = []
    users = []
    user =User.objects.filter(id = request.user.id).first()
    if user.is_superuser:
        student_list = Student.objects.all()
        teachers_list = Teacher.objects.all()
        users = User.objects.all()

    elif user.is_staff:
        teacher = Teacher.objects.filter(user = user)
        if teacher.exists():
            teacher_obj = teacher.first()
            teacher_class = teacher_obj.classSubject.all()
            for t_class in teacher_class:
                students = Student.objects.filter(classCurrent = t_class.studentClass)
                for dtud in students:
                    student_list.append(student_list)
        else:
            teachers_list = Teacher.objects.all()
            student_list = Student.objects.all()
            users = User.objects.all()

    elif Student.objects.filter(user= user).exists():
        student = Student.objects.filter(user= user).first()
        student_list  =Student.objects.filter(classCurrent = student.classCurrent)


    users_groups = []
    if users:
        for user in users:
            groups = user.groups.all()
            users_groups.append({'user':user, 'groups':groups})
    context = {'users_groups':users_groups, 'student_list':student_list, 'teachers_list':teachers_list}
    return render(request, 'Admin/list-student.html', context)

    # except:
    #     messages.error(request,'Something went wrong')
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/')
def studentAdd(request):
    departments = Department.objects.all()
    courses = SubjectClass.objects.all()
    context = {'departments':departments, 'courses':courses}
    return render(request, 'Admin/add-student.html', context)

@transaction.atomic()
def AddTeacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        bod = request.POST.get('bod')
        department = request.POST.get('department')
        class_level = request.POST.get('class_level')
        phone_no = request.POST.get('phone_no')
        email = request.POST.get('email')
        password = str(name).split(' ')[-1]
        User.objects.create_user(username=email, email=email, password=password)
        user = User.objects.filter(username = email).first()
        user.first_name = str(name).split(' ')[0]
        user.last_name = str(name).split(' ')[-1]
        user.save()
        no_subject_teacher_tought = SubjectClass.objects.all().count()
        department_obj = Department.objects.filter(id = department).first()
        Teacher.objects.create(name=  name, gender= gender, date_of_birth = bod, phone_number = phone_no, user = user, department = department_obj)
        teacher = Teacher.objects.filter(user = user).first()
        for i in class_level:
            subject_class_id = i
            subject_class_obj = SubjectClass.objects.filter(id = subject_class_id).first()
            teacher.classSubject.add(subject_class_obj)
        group =Group.objects.filter(name = 'Teachers').first()
        user.groups.add(group)

        messages.success(request,'Teacher is created successful')
        return redirect('studentlist')

@login_required(login_url='/')
def studentEdit(request, id):
    return render(request, 'Admin/edit-student.html')

@login_required(login_url='/')
def studentDelete(request, id):
    try:
        Student.objects.filter(id = id).delete()
        messages.success(request,'Student is deleted successful')
        return redirect('studentlist')

    except:
        messages.error(request,'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

