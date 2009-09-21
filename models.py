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
    challenger = models.ForeignKey(User, related_name = "challenger", 
                                   null = True, blank = True)
    challenged_users = models.TextField()
    
    def accept_all_challengers(self):
        """
        Returns True if this debate accepts all challengers, False otherwise
        """
        if self.challenger is not None:
            return False

        if not self.challenged_users.strip():
            # no challengers specified, all users can challenge
            return True

        return False

    def can_user_challenge(self, user):
        """
        Return True if a user can challenge this debate, False otherwise.
        A user can challenge a debate if the debate accepts all challengers or
        if the author of the debate specified the users name when creating
        the debate.
        """
        if self.challenger is not None:
            # debate already has challenger
            return False

        if isinstance(user, User):
            if user == self.instigator:
                # user cannot challenge own debate
                return False

            # user name in explicit challenged list
            if user.username in self.challenged_users.split(','):
                return True


        if self.accept_all_challengers():
            return True

        # user cannot challenge    
        return False

    def get_absolute_url(self):
        return "/debates/%d" % self.id

    def get_challenged_usernames(self):
        """returns a list of all usernames who were challenged"""
        return self.challenged_users.split(',')

    def last_post(self):
        try:
            return Entry.objects.filter(debate=self).order_by('-pub_date')[0]
        except IndexError:
            return None

    def __unicode__(self):
        return self.title

class Entry(models.Model):
    debate = models.ForeignKey(Debate)
    text = models.TextField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(auto_now_add = True)

    def author_role(self):
        if self.author == self.debate.instigator:
            return "instigator"
        else:
            return "challenger"

    def __unicode__(self):
        return "%s: %s, %s" % (self.debate.title, self.author, self.pub_date)

class Comment(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField()
    parent_entry = models.ForeignKey(Entry)
    parent_comment = models.ForeignKey('self', null = True, 
                                      blank = True)
    pub_date = models.DateTimeField(auto_now_add = True)
    parent_points = models.SmallIntegerField(choices = POINT_CHOICES, 
                                            default = 0)

    def __unicode__(self):
        return "%s, %s" % (self.author, self.pub_date)

class UserMessage(models.Model):
    recipient = models.ForeignKey(User, related_name="inbox_messages")
    sender = models.ForeignKey(User, related_name="sent_messages")
    message = models.TextField()
    date_read = models.DateTimeField(blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    """
    A debate profile for users containing debate site details for each user.
    To get a user profile, call use the get_for_user(user_name) class method
    """
    user = models.ForeignKey(User, related_name="debately_profile")
    join_date = models.DateTimeField(auto_now_add=True)
  
    @classmethod
    def get_profile_for_user(cls, profile_user):
        """
        Get debate user profile for given user.
        Creates new UserProfile for user if a user profile does not already exist.
        The preferred method for retrieving the debately profile is to user
        django.contrib.auth.models.User method debately_profile.get()
        """
        try:
            profile = UserProfile.objects.filter(user=profile_user)[0]
        except IndexError:
            profile = UserProfile(user=profile_user)
            profile.save()

        return profile

    #
    # some utility methods/examples to get user messages from profile
    def new_user_message_count(self):
        """returns count of unread messages for user"""
        return self.user.inbox_messages.filter(date_read=None).count()

    def get_user_messages(self):
        """all messages for user"""
        return self.user.inbox_messages.order_by("-date_sent")

    def get_sent_messages(self):
        """all sent messages"""
        return self.user.sent_messages.all()
        
    
