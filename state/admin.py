from django.contrib import admin
from .models import State
from django_summernote.admin import SummernoteModelAdmin

@admin.register(State)
class StateAdmin(SummernoteModelAdmin):

    summernote_fields = ('content')

