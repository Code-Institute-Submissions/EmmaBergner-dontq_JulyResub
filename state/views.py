from django.shortcuts import render
from.views import generic
from .models import State 
from django.views.generic.detail import DetailView

# Create your views here.
class ControlPage(DetailView):
    model = State 
    template_name = 'business.html'

