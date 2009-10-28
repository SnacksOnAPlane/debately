from django import template
import hashlib

register = template.Library()

@register.simple_tag
def avatar(user):
    return "<img class='avatar' src='http://www.gravatar.com/avatar/%s'>" % (hashlib.md5(user.email.strip().lower()).hexdigest())

@register.simple_tag
def smallavatar(user):
    return "<img class='avatar' src='http://www.gravatar.com/avatar/%s?s=50'>" % (hashlib.md5(user.email.strip().lower()).hexdigest())
