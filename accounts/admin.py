from django_summernote.admin import SummernoteModelAdmin
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class AdminProfile(SummernoteModelAdmin):
    summernote_fields = ('bio',)

