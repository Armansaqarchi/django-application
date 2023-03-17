from django.db.models.signals import post_save, post_delete
from .views import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail


 
@receiver(post_save, sender = User)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            email = user.email,
            name = user.username
        )


            

@receiver(post_delete, sender = Profile)
def delete_user(sender, instance, **kwargs):
    #getting the user object related to the profile
    user = instance.user
    user.delete()


@receiver(post_save, sender = Profile)
def updateProfile(sender, instance, created, **kwargs):

    #so why using created? remember when a user is updated,
    #  it might create a new profile using above function, and above function will make this function run again=> infinite loop
    if not created:
        profile = instance
        profile.user.first_name = profile.name
        profile.user.username = profile.name
        profile.user.email = profile.email






#this is the second method to connect the pre, post functions to the functions which you've defined
#you can do it directly using @receiver annotation above each function
###post_save.connect(profile_updated, sender = Profile)
###post_delete.connect(delete_user, sender = Profile)

#after this file written, need to let django know this file exists(see users.apps.py)