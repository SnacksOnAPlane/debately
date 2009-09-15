from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from models import Debate, Entry, Comment, UserProfile

def index(req):
    # list all debates by pubdate
    debates = Debate.objects.all().order_by('-pub_date')
    return render_to_response('index.html', 
                              RequestContext(req, {'debates': debates}))

def get_debate_points(debate, user):
    return Comment.objects.filter(parent_entry__debate = debate, 
                                  parent_entry__author = user, 
                                  parent_comment = None).aggregate(
                                      Sum('parent_points'))['parent_points__sum']

def get_comment_points(debate, user):
    raise Exception("not implemented yet")

def debate(req, id):
    debate = Debate.objects.get(id = id)
    c = { "debate": debate,
          "instigatorpoints": get_debate_points(debate, debate.instigator),
          "challengerpoints": get_debate_points(debate, debate.challenger),
          "entries": Entry.objects.filter(debate = debate)
         }
    return render_to_response('debate.html', RequestContext(req, c))


def userpage(req, user_name):
    """
    Shows user page for valid users, returns 404 if user is not found.
    """
    profile_user = get_object_or_404(User, username=user_name)
    user_profile = UserProfile.get_profile_for_user(profile_user)
    c = { 'profile_user': profile_user,
          'user_profile' : user_profile }
    return render_to_response('user_profile.html', 
                              RequestContext( req, c))
