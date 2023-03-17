from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def project_pagination(request, profiles, results):
    page = request.GET.get("page")

    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(paginator.num_pages)


    left_index = (int(page) - 3)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 3)
    #this attribute called num_pages specifies the number of pages in the paginator
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    #gonna use this custome_range in the template
    custom_range = range(left_index, right_index)

    return custom_range, profiles