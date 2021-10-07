from django import forms

from crispy_forms.layout import Submit, Div, Layout
from crispy_forms.helper import FormHelper
from django.forms.widgets import TextInput

class PersonDetailForm(forms.Form):
    gender  = forms.ChoiceField(
        label='What\'s your gender',
        choices=[('m', 'Male'), ('f', 'Female')]
    )
    dob = forms.DateField(
        label = 'Date of Birth',
        required=True,
        widget=TextInput(attrs={'placeholder': 'YYYY/MM/DD'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit(name='', value='Submit'))
        



class PersonForm(forms.Form):
    firstname = forms.CharField(
        label='Enter first name',
        required=True,
        max_length=30,
    )
    lastname = forms.CharField(
        label='Enter last name',
        required=True,
        max_length=30,
    )
    username = forms.CharField(
        label='Enter username',
        required=True,
        max_length=20,    
    )
    email = forms.EmailField(
        label='Enter email address',
        required=True,
        max_length=100
    )
    password1 = forms.CharField(
        label='Enter password',
        required=True,
        max_length=20,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Enter password again',
        required=True,
        max_length=20,
        widget=forms.PasswordInput()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit(name='submit', value='Submit'))


class BlogForm(forms.Form):
    title = forms.CharField(
        label='Title',
        max_length=100,
    )
    blog = forms.CharField(
        label='What\'s on your mind',
        widget=forms.Textarea()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('', 'Post')) 


class LoginForm(forms.Form):
    username = forms.CharField(label='Enter your username',) 
    password = forms.CharField(label='Enter your password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('', 'Login'))
