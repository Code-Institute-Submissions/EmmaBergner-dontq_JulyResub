from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import State

# Create your views here.


class ControlPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        print("hello")
        
        queryset = State.objects.all()
        state = get_object_or_404(queryset, id=2)
        if (request.GET.get('mybtn')):
            print("world")
            state.current = state.current+1
            state.save()
        context = {
            'current': state.current
        }
        return render(request, 'business.html', context)



def request_page(request):
    if(request.GET.get('mybtn')):
        mypythoncode.mypythonfunction(int(request.GET.get('mytextbox')))
    return render(request, 'myApp/templateHTML.html')