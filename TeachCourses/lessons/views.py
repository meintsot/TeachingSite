from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib import messages
from .security import check_email, get_random_password, get_user
from django.core.mail import send_mail

def IndexView(request):
    announcements = models.Announcement.objects.order_by('-pub_date')
    return render(request, 'lessons/index.htm', {'announcements': announcements})

def LessonsView(request):
    categories = models.Category.objects.all()
    return render(request, 'lessons/lessons.htm', {'categories': categories})

def HomeWorkView(request):
    categories = models.Category.objects.all()
    return render(request, 'lessons/homework.htm', {'categories': categories})

def LogoutView(request):
    logout(request)
    return redirect(reverse('index'))

def RegisterView(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            token = models.Token.objects.filter(value=request.POST['token'])
            if token:
                token = token[0]
            if token:
                user = form.save(commit=False)
                user.email = request.POST['email']
                if not check_email(request.POST['email']):
                    messages.error(request, "Email is not correct.")
                    return redirect(reverse('register'))
                user.save()
                token.delete()
                user = authenticate(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password1"))
                if user is not None:
                    login(request, user)
                else:
                    return Http404()
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Token does not exist. Make sure that your token is correct and you own a token or contact with the teacher.')
                return redirect('.')
        else:
            return redirect('.')
    else:
        return render(request, 'lessons/register.htm', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, "Username and password do not match.")
            return redirect(".")
    return render(request, 'lessons/login.htm')

def ChangePasswordView(request):
    if request.method == 'POST':
        username = request.user.username
        curpass = request.POST.get("curpass")
        user = authenticate(username=username, password=curpass)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if not password1 or not password2:
            messages.error(request, "New password can't be blank")
        if user is None:
            messages.error(request, "Current password is not valid.")
            return redirect(reverse('changepw'))
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('changepw'))
        if len(password1) < 8:
            messages.error(request, "New password must me at least 8 characters long.")
            return redirect(reverse('changepw'))
        request.user.set_password(password1)
        request.user.save()
        user = authenticate(username=username, password=password1)
        login(request, user)
        messages.success(request, "Password changed successfully")
        return redirect(reverse('changepw'))
    return render(request, 'lessons/changepw.htm')

def ForgotPasswordView(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        if not check_email(email):
            messages.error(request, "Email is not valid!")
            return redirect(reverse('forgotpw'))
        print(email)
        password = get_random_password(8)
        username = request.POST['username']
        user = get_user(username)
        user.set_password(password)
        user.save()    
        send_mail(
            'TeachingCourses:Forgot Password',
            'Hey there, your new password has successfully been set and it is: {}'.format(password),
            'meintsot01@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, "A new password has been sent to your email. Use this password to log in and then go to Change password and set a new one.")
        return redirect(reverse('login'))
    return render(request, 'lessons/forgotpw.htm')