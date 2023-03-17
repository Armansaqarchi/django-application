from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import search_project
from .utils import project_pagination
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def projects(request):
    
    projects, search_query = search_project(request)
    custom_range, projects = project_pagination(request, projects, 2)
    context = {"projects" : projects, "search_query" : search_query, "custom_range" : custom_range}
    return render(request, "projects.html", context)


def project(request, pk):
    
    review_form = ReviewForm()
    project_obj = Project.objects.get(pk=pk)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()
        messages.success("Review successfully submitted")
    
    tags = project_obj.tags.all()
    context = {"project_obj" : project_obj, "tags" : tags, "form"  : review_form}
    return render(request, 'project.html', context)


@login_required(login_url="login")
def create_project(request):
    #as this method takes responsiblity to save and load the model form
    #we need to aknowledge that what type of request we are getting.

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if(form.is_valid):
            project = form.save(commit = False)
            project.owner = request.user.profile
            project.save()
            return redirect("projects")


    form = ProjectForm()
    context = {"form" : form}
    return render(request, "project_form.html", context)

def update_project(request, pk): 
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance = project)

    if(request.method == "POST"):
        form = ProjectForm(request.POST, request.FILES, instance = project)
        if(form.is_valid):
            form.save()
            project.save()
            return redirect("projects")
    
    context = {"form" : form}
    return render(request, "project_form.html", context = context)

def delete_project(request, pk):
    #cause we are doing delete stuff, we need to get the project object
    profile = request.user.profile
    project_obg = profile.project_set.get(id = pk)
    context = {"project" : project_obg}
    if request.method == "POST":
        project_obg.delete()
        return redirect("projects")


    return render(request, "delete_project.html", context = context)



