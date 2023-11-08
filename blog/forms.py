from .models import Comment

from django import forms

from django_summernote.widgets import SummernoteWidget


class EmailPostForm(forms.Form):
    name = forms.CharField()
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=SummernoteWidget())
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    ''' форма для ввода поискового запроса '''
    query = forms.CharField()
