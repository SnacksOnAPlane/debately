from django import template

register = template.Library()

@register.filter("can_user_challenge")
def can_user_challenge(debate, user):
    return debate.can_user_challenge(user)
