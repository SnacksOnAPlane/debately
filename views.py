from django.db.models import Sum
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from models import Debate, Entry, Comment, UserProfile

def index(req):
  # list all debates by pubdate
  debates = Debate.objects.all().order_by('-pub_date')
  return render_to_response('index.html', {'debates': debates})

def getDebatePoints(debate, user):
  return Comment.objects.filter(parentEntry__debate = debate, parentEntry__author = user, parentComment = None).aggregate(Sum('parentPoints'))['parentPoints__sum']

def getCommentPoints(debate, user):
  raise Exception("not implemented yet")

def debate(req, id):
  debate = Debate.objects.get(id = id)
  c = { "debate": debate,
      "instigatorpoints": getDebatePoints(debate, debate.instigator),
      "challengerpoints": getDebatePoints(debate, debate.challenger),
      "entries": Entry.objects.filter(debate = debate)
      }
  return render_to_response('debate.html', c)


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
