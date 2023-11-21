from .models import Comment

from django import forms

from django_summernote.widgets import SummernoteWidget


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25,
                           required=True,
                           widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Имя'}))
    from_email = forms.EmailField(required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    to_email = forms.EmailField(required=True,
                                widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Кому'}))
    comment = forms.CharField(required=False,
                              widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Комментарий'}))


class CommentPostForm(forms.ModelForm):
    body = forms.CharField(required=True,
                           widget=SummernoteWidget(
                               attrs={"class": "form-control", 'summernote': {'width': '100%', 'height': '300px'}}))

    class Meta:
        model = Comment
        fields = ['body']


