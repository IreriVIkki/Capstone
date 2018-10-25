from django.shortcuts import HttpResponse, render, redirect, get_object_or_404, reverse, get_list_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .forms import *
from .models import *
import datetime

# Create your views here.


def home(request):
    data = {}
    leaders = Profile.leader_board()
    q_form = QuestionForm()
    user = request.user
    questions = Question.all_questions()
    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        print(q_form.is_valid())
        if q_form.is_valid():
            query = q_form.save(commit=False)
            query.save_question(user)
            # set the value of form is valid to true for ajax to check
            data['form_is_valid'] = True

            questions = Question.all_questions()
            data['home_update'] = render_to_string('includes/all_questions_partial.html', {
                'questions': questions
            })
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False
    context = {
        'user': user,
        'leaders': leaders,
        'q_form': q_form,
        'questions': questions,
    }
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.create_profile(user)
            print(user.profile.user_name)
            return redirect('login')

    form = MyRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def edit_profile(request):
    form = ProfileForm()
    user = request.user
    if request.user.is_authenticated():
        if request.method == "POST":
            try:
                profile = user.profile
                form = ProfileForm(instance=profile)
                form = ProfileForm(
                    request.POST, request.FILES, instance=profile)
                if form.is_valid():
                    update = form.save(commit=False)
                    update.user = user
                    update.save()
            except:
                form = ProfileForm(request.POST, request.FILES)
                print(form.is_valid())
                if form.is_valid():
                    profile = form.save(commit=False)
                    profile.save_profile(user)
            return redirect('home')
    else:
        form = ProfileForm()

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'profile_edit.html', context)


def profile(request, user_id, username):
    user = get_object_or_404(User, id=user_id)
    if not request.user.is_authenticated():
        return redirect("login")
    try:
        profile = user.profile
    except:
        return redirect('edit_profile')

    user = User.objects.get(pk=user.id)
    form = CheckStatusForm()
    form1 = ChecklistForm()
    # posts = Post.objects.all()
    context = {
        'user': user,
        'form': form,
        'form1': form1,
        # 'posts': posts,
        'profile': profile
    }
    return render(request, 'profile.html', context)
