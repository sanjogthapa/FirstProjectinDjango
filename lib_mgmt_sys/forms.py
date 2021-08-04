# from django.forms import Form
# from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput

from lib_mgmt_sys.models import *



class AuthorAddForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class BookModelForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('name', 'author', 'price', 'no_pgs', 'cover_photo')    #__all__ gareko vaye books model ko sabai attributes linthyo

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    repeat_password = forms.CharField(widget=PasswordInput)
    role = forms.ChoiceField(choices=(('Student', 'Student'), ('Librarian', 'Librarian')))

    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name','password')

    def clean(self):
        cleaned_data= super(UserModelForm,self).clean()
        password= cleaned_data['password']
        repeat_password= cleaned_data['repeat_password']

        if password != repeat_password:
            raise forms.ValidationError('Password does not match')



    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            raise forms.ValidationError('Password too small')

        if ' ' in password:
            raise forms.ValidationError('Password can\'t have space')


        return password


