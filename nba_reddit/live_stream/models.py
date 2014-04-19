from django.db import models
from django.contrib import admin
from django.forms import ModelForm, forms

class InsertComment(models.Model):

    comment = models.TextField()

class InsertCommentForm(ModelForm):

    class Meta:
        model = InsertComment
        widgets = {
            'comment': forms.Textarea(attrs={'style': "width: 350px", 'rows': 3, }),
        }
        fields = ['comment']