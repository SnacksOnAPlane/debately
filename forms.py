from django import forms

class CreateDebateForm(forms.Form):
    title = forms.CharField(max_length=100)
    summary = forms.CharField(widget=forms.Textarea)

class DebateEntryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
