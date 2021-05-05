from django import forms

class UserRegister(forms.Form):
    name = forms.CharField(label='Your Name', max_length=50)
    media = forms.FileField(label='Upload your Picture' ) 


class SignupForm(forms.Form):

    firstname = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    lastname = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'placeholder': 'User name'}))
    email = forms.EmailField(label='Enter Email ID', widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))
    password1 = forms.CharField(label='Password', widget=forms.TextInput(attrs={'placeholder': 'password', 'type': 'password'}))
    password2 = forms.CharField(label='Enter Password Again', widget=forms.TextInput(attrs={'placeholder': 'Same password as above', 'type': 'password'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Enter Username', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'placeholer': 'Enter Password', 'type': 'password', 'autocomplete': 'off'}))


