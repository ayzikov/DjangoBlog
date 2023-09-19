from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField()
    from_email = forms.EmailField()
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)

