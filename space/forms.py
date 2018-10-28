from django import forms
# fill in custom user info then save it
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
import random
import string

csrf = ''.join(random.choices(string.ascii_lowercase +
                              string.ascii_uppercase + string.digits, k=64))


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.save()

        return user


class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        exclude = []


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        widgets = {
            'd_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }
        exclude = ['user', 'coins']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['author', 'date_asked', 'views',
                   'answered', 'duplicate', 'upvotes', 'downvotes']


class ChecklistForm(forms.ModelForm):

    task_id = forms.CharField()

    class Meta:
        model = Checklist
        exclude = ['task']
        widgets = {
            'status': forms.CheckboxInput(
                attrs={'onclick': 'this.form.submit();'}),
        }


class AnswerForm(forms.ModelForm):

    query_id = forms.CharField()

    class Meta:
        model = Answer
        exclude = ['author', 'date_answered', 'views',
                   'question', 'verified', 'upvotes', 'downvotes']
