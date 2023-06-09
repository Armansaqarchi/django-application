from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save, post_delete


class Profile(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank = True)
    email = models.EmailField(max_length=500, null=True, blank = True)
    info = models.CharField(max_length= 200, null=True, blank = True)
    bio = models.TextField(null=True, blank = True)
    location = models.CharField(max_length = 200, null=True, blank = True)
    profile_image = models.ImageField(null=True, blank = True, default="images/profiles/user-default.png")
    social_github = models.CharField(max_length=200, null=True, blank = True)
    social_youtube = models.CharField(max_length=200, null=True, blank = True)
    social_linkedin = models.CharField(max_length=200, null=True, blank = True)
    social_website = models.CharField(max_length=200, null=True, blank = True)
    created = models.DateTimeField(null=True, blank = True, auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4,
     editable=False, unique = True, primary_key = True)

    def __str__(self) -> str:
        return self.user.username



class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank = True)
    name = models.CharField(max_length=200, null=True, blank = True)
    description = models.TextField(null=True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default = uuid.uuid4, editable=False, primary_key=True, unique=True)


    def __str__(self):
        return str(self.name)
    


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recepient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.subject 
    

    class Meta:
        ordering = ["is_read", "-created"]