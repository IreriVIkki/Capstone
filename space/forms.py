from django import forms
# fill in custom user info then save it
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


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


class CheckStatusForm(forms.ModelForm):

    class Meta:
        model = CheckStatus
        exclude = ['label']
        widgets = {
            'status': forms.CheckboxInput(
                attrs={'onclick': 'this.form.submit();'}),
        }


class ChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        exclude = ['task']
