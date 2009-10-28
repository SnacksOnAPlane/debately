from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse

from models import Debate, Entry, Comment, UserMessage, UserProfile
from forms import CreateDebateForm, DebateEntryForm, CreateCommentForm

def index(req):
    """list all debates by pubdate"""

    # TODO: this is temporary, just to ensure a user profile 
    # exists for authenticated users
    if req.user.is_authenticated():
        UserProfile.get_profile_for_user(req.user)

    debates = Debate.objects.all().order_by('-pub_date')
    return render_to_response('index.html', 
                              RequestContext(req, {'debates': debates}))

def get_debate_points(debate, user):
    return Comment.objects.filter(parent_entry__debate = debate, 
                                  parent_entry__author = user, 
                                  parent_comment = None).aggregate(
                                      Sum('parent_points'))['parent_points__sum'] or 0

def get_comment_points(debate, user):
    raise Exception("not implemented yet")


@login_required
def challenge_debate(req, id):
    """accept challenge to debate"""
    debate = get_object_or_404(Debate, pk=id)
    #TODO: should return better error than 404
    if debate.challenger is not None:
        raise Http404("Invalid Request")

    if not debate.can_user_challenge(req.user):
        raise Http404("Invalid Request")
    
    debate.challenger = req.user
    debate.save()
    return HttpResponseRedirect(debate.get_absolute_url())


def debate(req, id):
    debate = Debate.objects.get(id = id)
    userCanPostEntry = req.user == debate.instigator or req.user == debate.challenger
    if req.method == "POST":
        form = DebateEntryForm(req.POST)
        if form.is_valid() and userCanPostEntry:
            Entry.objects.create(debate = debate, text = form.cleaned_data['text'], author = req.user)
    entryForm = DebateEntryForm()
    c = { "debate": debate,
          "instigatorpoints": get_debate_points(debate, debate.instigator),
          "challengerpoints": get_debate_points(debate, debate.challenger),
          "entries": Entry.objects.filter(debate = debate),
          "userCanPostEntry": userCanPostEntry,
          "userCanComment": req.user.is_authenticated() and not userCanPostEntry,
          "entryForm": entryForm,
         }
    return render_to_response('debate.html', RequestContext(req, c))


def userpage(req, user_name):
    """
    Shows user page for valid users, returns 404 if user is not found.
    """
    profile_user = get_object_or_404(User, username=user_name)
    UserProfile.get_profile_for_user(profile_user)
    c = { 'profile_user': profile_user }
    return render_to_response('user_profile.html', 
                              RequestContext( req, c))

@login_required
def usermessages(req):
    """
    Shows messages for user, returns 404 if user is not found
    """
    ctx = {}
    return render_to_response('user_messages.html', 
                              RequestContext( req, ctx))


@login_required
def create_debate(req):
    if req.method == "POST":
        form = CreateDebateForm(req.POST)
        if form.is_valid():
            deb = Debate(title = form.cleaned_data['title'], 
                         summary = form.cleaned_data['summary'], 
                         instigator = req.user,
                         challenged_users = form.cleaned_data['challenged_users'])
            deb.save()
            
            if not deb.accept_all_challengers():
                # add message for each challenged user.
                for uname in deb.get_challenged_usernames():
                    u = User.objects.get(username=uname)
                    msg = UserMessage(recipient=u,
                                      message="new challenge: %s" % deb.title,
                                      sender=deb.instigator)
                    msg.save()
            
            return HttpResponseRedirect('/')
    else:
        form = CreateDebateForm()

    return render_to_response("create_debate.html", 
                              RequestContext(req, {"form": form}))

@login_required
def create_comment(req, entry):
    if req.method == "POST":
        entry = Entry.objects.get(pk=entry)
        form = CreateCommentForm(req.POST)
        if form.is_valid():
            comment = Comment(text = form.cleaned_data['text'],
                              parent_entry = entry,
                              author = req.user,
                              parent_points = form.cleaned_data['points'])
            comment.save()
            debatenum = entry.debate.id
            return HttpResponseRedirect('/debates/%s' % debatenum)
    else:
        form = CreateCommentForm()
        return render_to_response("create_comment.html",
                                  RequestContext(req, {"form": form}))
