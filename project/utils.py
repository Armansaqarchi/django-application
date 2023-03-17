from .models import Project
from django.shortcuts import render
from .models import Tag
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def search_project(request):
    search_query = ""

    if(request.GET.get("search_query")):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains = search_query)

    projects = Project.objects.distinct().filter(Q(owner__name__icontains = search_query) | Q(title__icontains = search_query) | 
    Q(tags__in = tags) | Q(description__icontains=search_query))


    return projects, search_query


def project_pagination(request, projects, results):
    page = request.GET.get("page")

    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(paginator.num_pages)


    left_index = (int(page) - 3)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 3)
    #this attribute called num_pages specifies the number of pages in the paginator
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    #gonna use this custome_range in the template
    custom_range = range(left_index, right_index)

    return custom_range, projects