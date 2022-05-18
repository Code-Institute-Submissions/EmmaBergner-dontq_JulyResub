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
        if (request.GET.get('mybtn') and state.current>0):
            state.current = state.current-1
        if (request.GET.get('mybtng')):
            state.current = state.current+1  
        if (request.GET.get('myreset')):
            state.current = state.current=0
        state.save()  
        context = {
            'current': state.current
        }
        return render(request, 'business.html', context)

class UserPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        print(self)
        print(request)
        print(args)
        print(kwargs)
        queryset = State.objects.all()
        state = get_object_or_404(queryset, id=2)
        context = {
            'current': state.current,
            'next': state.next
        }
        state.next = state.next+1 
        state.save()  
        return render(request, 'user.html', context)

