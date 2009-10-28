from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from models import POINT_CHOICES


class ChallengedUsersField(forms.Field):
    """
    Field to input a comma separated list of users to challenge.
    """

    def clean(self, value):
        """
        ensure all entries are valid users. Return normalized csv list
        of usernames.
        """
        # no challengers (empty string) is O.K.
        if not value.strip():
            return ""

        ulist = [u.strip() for u in value.split(',')]
        for u in ulist:
            try:
                User.objects.get(username=u)
            except ObjectDoesNotExist:
                raise forms.ValidationError("User %s does not exist" % u)

        return ",".join(ulist)


class CreateDebateForm(forms.Form):
    """
    form for creating new debates.
    """
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)
    challenged_users = ChallengedUsersField(
        help_text='Separate multiple usernames with commas. Leave blank \
                   to accept all challengers')


class DebateEntryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

class CreateCommentForm(forms.Form):
    points = forms.ChoiceField(choices=POINT_CHOICES, initial=0)
    text = forms.CharField(widget=forms.Textarea)
