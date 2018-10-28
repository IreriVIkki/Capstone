from django.shortcuts import HttpResponse, render, redirect, get_object_or_404, reverse, get_list_or_404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .forms import *
from .models import *
import datetime
from django.views.generic import TemplateView
from .mixins import AjaxFormMixin


# Create your views here.


@csrf_protect
def home(request):
    data = {}
    leaders = Profile.leader_board()
    q_form = QuestionForm()
    user = request.user
    questions = Question.all_questions()
    tasks = Task.all_tasks()
    item_f = ChecklistForm()
    answer_f = AnswerForm()
    if request.method == 'POST':
        answer_f = AnswerForm(request.POST)
        if answer_f.is_valid():
            answer = answer_f.save(commit=False)
            query_id = answer_f.cleaned_data['query_id']
            answer.save_answer(query_id, user)

    if request.method == 'POST':
        item_f = ChecklistForm(request.POST)
        if item_f.is_valid():
            item = item_f.save(commit=False)
            task_id = item_f.cleaned_data['task_id']
            item.save_item(task_id)
            data['form_is_valid'] = True
            tasks = Task.all_tasks()

            data['items_update'] = render_to_string('includes/tasks_partial.html', {
                'tasks': tasks
            })
            return JsonResponse(data)

    # form adding a new question
    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        if q_form.is_valid():
            query = q_form.save(commit=False)
            query.save_question(user)

            data['form_is_valid'] = True

            questions = Question.all_questions()

            data['home_update'] = render_to_string('includes/all_questions_partial.html', {
                'questions': questions
            })
            return JsonResponse(data)
        else:
            data['form_is_valid'] = False

    if request.method == 'POST' and request.POST['status']:
        item_id = request.POST['task_id']
        print('here first', item_id)
        item = Checklist.get_item(item_id)
        item.complete_item()
        data['form_is_valid'] = True
        tasks = Task.all_tasks()

        data['items_update'] = render_to_string('includes/tasks_partial.html', {
            'tasks': tasks
        })
        return JsonResponse(data)
    context = {
        'csrf': csrf,
        'user': user,
        'tasks': tasks,
        'item_f': item_f,
        'leaders': leaders,
        'q_form': q_form,
        'questions': questions,
        'answer_f': answer_f
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
    print(csrf)
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
    form1 = ChecklistForm()
    # posts = Post.objects.all()
    context = {
        'user': user,
        'form1': form1,
        # 'posts': posts,
        'profile': profile
    }
    return render(request, 'profile.html', context)


class MoriSpaceView(AjaxFormMixin, TemplateView):
    # setting up templates to be used
    template_name = 'profile.html'

    # setting up forms to be displayed
    q_form = QuestionForm()
    item_f = ChecklistForm()
    answer_f = AnswerForm()

    # form_class = AnswerForm
    tasks = Task.all_tasks()
    items = Checklist.all_items()
    leaders = Profile.leader_board()
    questions = Question.all_questions()

    # adding all that crap to the context object that will be rendered
    context = {}
    context['items'] = items
    context['tasks'] = tasks
    context['leaders'] = leaders
    context['questions'] = questions
    context['form'] = item_f

    def get(self, request):
        return render(request, self.template_name, self.context)


class UpdateItemsView(MoriSpaceView):

    # override form class to pass the required form for this function to work and the destination url as well
    form_class = ChecklistForm
    target_url = 'includes/test_partial.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            # save the form and submit the new item to the database
            item = form.save(commit=False)
            task_id = form.cleaned_data['task_id']
            item.save_item(task_id)
            items = Checklist.all_items()
            # update context items to include the newly submited item before rendering
            self.context['items'] = items
            # create an updated html sting including the newly updated items
            html = render_to_string(self.target_url, self.context)
            # return the html string as success data to subimt form ajax call
            return HttpResponse(html)
        return render(request, self.template_name, self.context)
