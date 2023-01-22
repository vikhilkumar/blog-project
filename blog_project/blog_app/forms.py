from dataclasses import field
from email.message import Message
from pyexpat import model
from django import forms
class EmailSendForm(forms.Form):
    Name=forms.CharField()
    From=forms.CharField()
    To=forms.CharField()
    Message=forms.CharField(required=False,widget=forms.Textarea)

    #Above EmailSendForm Data will be stored in cleaned_data(this is dict form)
    #Below CommentForm data will be stored in database table since they are model forms.

from .models import Comment #Here we using model forms
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','body')