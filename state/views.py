from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import State 

# Create your views here.
class ControlPage(View):
    model = State 
    template_name = 'business.html'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        queryset = State.objects.all()
        state = get_object_or_404(queryset, id=2)
        
        return render(request, 'business.html')
        return render(request, 'user.html')
