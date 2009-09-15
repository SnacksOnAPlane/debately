from django.contrib.auth.models import User
from django.db import models


POINT_CHOICES = (
    (-1, -1),
    (0, 0),
    (1, 1),
)


class Debate(models.Model):
    title = models.CharField(max_length = 200)
    summary = models.TextField() #not for the first entry! just a summary, please
    pub_date = models.DateTimeField(auto_now_add = True)
    instigator = models.ForeignKey(User, related_name = "instigator")
    challenger = models.ForeignKey(User, related_name = "challenger")


class Entry(models.Model):
    debate = models.ForeignKey(Debate)
    text = models.TextField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add = True)


class Comment(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField()
    parent_entry = models.ForeignKey(Entry)
    parent_comment = models.ForeignKey('self', null = True, 
                                      blank = True)
    pub_date = models.DateTimeField(auto_now_add = True)
    parent_points = models.SmallIntegerField(choices = POINT_CHOICES, 
                                            default = 0)


class UserProfile(models.Model):
    """
    A debate profile for users containing debate site details for each user.
    To get a user profile, call use the get_for_user(user_name) class method
    """
    user = models.ForeignKey(User)
    join_date = models.DateTimeField(auto_now_add=True)
  
    @classmethod
    def get_profile_for_user(cls, profile_user):
        """
        Get debate user profile for given user.
        Creates new UserProfile for user if a user profile does not already exist.
        """
        try:
            profile = UserProfile.objects.filter(user=profile_user)[0]
        except IndexError:
            profile = UserProfile(user=profile_user)
            profile.save()

        return profile
    
