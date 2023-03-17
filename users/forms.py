from .models import Profile
from django import forms
from .models import Skill, Message
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class custom_user_creation_form(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]
        labels = {"first_name" : "Name", "username" : "Username"}

    #actually to make this form a little better, gonna customize the every single widget thr form has.
    def __init__(self, *args, **kwargs):
        #calling parent calss's init method
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # to make every widget in the form look like better, there is a method customizes the widget:
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["name", "email", "info", "bio", "location", "profile_image", "social_github", "social_youtube", "social_linkedin", "social_website"]

    def __init__(self, *args, **kwargs) -> None:
        super(ProfileForm, self).__init__(*args , kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})



class SkillForm (ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs) -> None:
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, *kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({"class" : "input"})
