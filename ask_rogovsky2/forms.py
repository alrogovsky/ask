from django import forms
from ask.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ask.models import Question, Answer

class SignUp(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(max_length=70)
    pass1 = forms.CharField(widget=forms.PasswordInput())
    pass2 = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already in use')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise forms.ValidationError('Invalid email')

    def clean(self):
        cleaned_data = super(SignUp, self).clean()
        pass1 = cleaned_data['pass1']
        pass2 = cleaned_data['pass2']
        if pass1 != pass2:
            msg = 'Passwords didn`t match'
            self._errors["pass2"] = self.error_class([msg])
        return cleaned_data


class EditProfile(forms.Form):
    name = forms.CharField(label='First name', max_length=30)
    l_name = forms.CharField(label='Last name', max_length=40)
    email = forms.EmailField(max_length=70)
    avatar = forms.ImageField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise forms.ValidationError('Invalid email')


class Ask(ModelForm):
    tags = forms.CharField(required=False)
    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == "":
            raise forms.ValidationError('You can not submit an empty answer!')
        else:
            return text