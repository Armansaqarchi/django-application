from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):

    #owner of the project:
    owner = models.ForeignKey(Profile, null= True, blank= True, on_delete = models.SET_NULL)



    #need the followings in order to make migration and create our database:
    #1) title, 2)description, 3)demo_ling, 4)source_link, 5)created, 6)unique id
    title = models.CharField(max_length=200)

    #COULD BE NULL AND BLANK
    description = models.TextField(null = True, blank = True)
    demo_link = models.CharField(max_length=2000, null = True, blank=True)
    source_link = models.CharField(max_length=2000, null = True, blank=True)
    #can submit the time this item was created

    featured_image = models.ImageField(null = True, blank = True, default= "images/profiles/user-default_YS9Vr6e.png")
    created = models.DateTimeField(auto_now_add=True)
    #in order to use many to many relationship, note that when the model is created before the target class,
    #we can specify the target model by saying the class itself
    #but when its createed after, we call specify using quots and the same name as the model.
    tags = models.ManyToManyField('Tag', blank=True)
    #total number of votes
    vote_total = models.IntegerField(default = 0, null=True, blank = True)
    #total percentage of votes
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key=True, editable=False)


    def __str__(self):
        return self.title


    #now we need to make this migrations and migrate
    ### note that after its done, we need to get this tied with the admin panel
    #we can do this using the admin module in admin py file



class Review(models.Model):

    
    
    VOTE_TYPE = (("up", "Up Vote"), ("down", "Down Vote"))

    #owner(which is a profile isnt created yet)
    #lets create many to one relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    body = models.TextField(null = True, blank = True)
    #there is an argument which takes the choices as a tuple
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add = True)
    
    #id  type of uuid, primary key? can be edited? is it unique?
    id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]
    
    def __str__(self):
        return self.value


#lets add another model which is tag:
class Tag(models.Model):
    name = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default=uuid.uuid4, unique = True, primary_key = True, editable=True)

    def __str__(self):
        return self.name



