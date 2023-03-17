from django.shortcuts import render, redirect
from .models import Profile, Skill
from .forms import ProfileForm, SkillForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import custom_user_creation_form
from .utils import project_pagination




def login_page(request):

    page = "login"
    form = custom_user_creation_form()

    #this if runs when the user is logged in and trying to login again
    if request.user.is_authenticated:
        return redirect("Profiles")


    #which means while the user are to send his user password in login form
    if request.method == 'POST':
        
        username = request.POST['username'].lower()
        password = request.POST['password']
        

        
        try:
            user = User.objects.get(username=username)
            Profile.objects.get(user = user)
        except User.DoesNotExist:
            messages.error(request, "username does not exist")
        

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")
        

    context = {"page" : page, "form" : form}
    return render(request, 'users/login_register.html', context = context)



def profiles(request):

    search_query = ""
    skills = ""
    
    if request.GET.get("search_query"):
        
        search_query = request.GET.get("search_query")

    skills = Skill.objects.distinct().filter(name__iexact=search_query)
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | Q(info__icontains=search_query) | Q(skill__in=skills))
    custom_range, profiles = project_pagination(request, profiles, 3)

    context = {"profiles" : profiles, "custom_range" : custom_range}

    return render(request, "users/profiles.html", context=context)



def user_profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    top_skills = profile.skill_set.exclude(description__exact = "")
    other_skills = profile.skill_set.filter(description = "")
    context = {"profile" : profile, "top_skills" : top_skills, "other_skills" : other_skills}
    return render(request, "users/profile.html", context=context)

def logout_page(request):
    logout(request)
    messages.success(request, "user was successfully logged out")
    return redirect("login")


def register_user(request):
    page = "register"
    form = custom_user_creation_form()
    
    if(request.method == "POST"):
        form = custom_user_creation_form(request.POST)
        if(form.is_valid()):
            user = form.save(commit = False)
            user.username.lower()
            user.save()

            messages.success(request, "User account was created")

            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "an error has occured while registeration")
    
        
    context = {"page" : page, "form" : form}
    return render(request, "users/login_register.html", context = context)

@login_required(login_url="login") 
def user_account(request):

    #using profile to make the account ready...
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {"profile": profile, "skills" : skills, "projects": projects}
    return render(request, "users/account.html", context = context)

@login_required(login_url="login")
def edit_profile (request):

    profile = request.user.profile
    
    form = ProfileForm(instance = profile)
    context = {"form" : form}


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect("account")
        else:
            print("is not valid")

    return render(request, "users/profile_form.html", context = context)


@login_required(login_url="login")
def create_skill (request):
    profile = request.user.profile
    form = SkillForm()
    context = {"form" : form}

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.success(request, "skill was created successfully")
            return redirect("account")
        else:
            print("is not valid")

    return render(request, "users/skill_form.html", context = context)


def update_skill (request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(pk=pk)
    form = SkillForm(instance = skill)
    
    if(request.method == "POST"):
        form = SkillForm(request.POST, instance = skill)
        if(form.is_valid()):
            form.save()
            messages.success(request, "skill was updated successfully")
            return redirect("account")
    
    messages.error("unable to update skill")
    context = {"form" : form}
    return render(request, "users/skill_form.html", context = context)


def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(pk=pk)
    
    if(request.method == "POST"):
        skill.delete()
        messages.success(request, "skill was deleted successfully")
        return redirect("account")
    
    context = {"skill" : skill}
    return render(request, "users/delete_skill.html", context= context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messages = profile.messages.all()
    unread_messages = messages.filter(is_read=False).count()
    context = {"R_messages": messages, "unread_messages" : unread_messages}
    return render(request, "users/inbox.html", context=context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not  message.is_read:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context=context)

def create_project(request, pk):
    recepient = Profile.objects.get(pk = pk)
    sender = request.user.profile
    
    if request.method == "POST":
        messageForm = messageForm(request.POST)
        if messageForm.is_valid():
            message = messageForm.save()
            message.sender = sender
            message.recepient = recepient
            if sender:
                message.email = sender.email
                message.name = sender.name
            message.save()   
            messages.success(request, 'your message has been successfully sent to the user')
            return redirect("profile", pk = recepient.id)

    messageForm = messageForm() 
    context = {"recepient" : recepient, "form" : messageForm}
    return render(request, "users/message_form.html", context)
