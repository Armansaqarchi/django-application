from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from project.models import Project, Review, Profile
from .serializers import ProjectSerializer



@api_view(["GET", "POST"])
def getRoutes(request):

    routes = [
        {"GET" : "api/projects/id"},
        {"VOTE" : "api/projects/id/vote"},
        {"GET" : "api/projects"},
        {"GET" : "api/users/token/refresh"},
        {"GET" : "api/users/token"}
    ]

    return Response(routes)


@api_view(http_method_names=["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getProjects(request):
    projects = Project.objects.all()
    #need to serialize that to json formant
    serializedProjects = ProjectSerializer(projects, many=True)

    return Response(serializedProjects.data)

@api_view(http_method_names=["GET"])
def getProject(requset, pk):
    project = Project.objects.get(pk = pk)
    serializedProject = ProjectSerializer(project, many = False)
    return Response(serializedProject.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_project(request, pk):
    project = Project.objects.get(pk=pk)
    owner = request.user.profile
    

    review, created = Review.objects.get_or_create(
        owner = owner,
        project = project
    )

    review.value = request.data["value"]
    review.save()

    print("DATA:", request.data)
    
    response = ProjectSerializer(project, many=False)
    return Response(response.data)