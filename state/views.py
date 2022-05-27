from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from .models import State
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages


# Create your views here.

@method_decorator(login_required, name='get')
class ControlPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        state = get_object_or_404(State, business = request.user)
        if (request.GET.get('mybtn') and state.current > 0):
            state.current = state.current-1
        if (request.GET.get('mybtng')):
            state.current = state.current+1
        if (request.GET.get('myreset')):
            state.current = 0
            state.next = 0
        if (request.GET.get('mylogout')):
            logout(request)
            return redirect('/')
        state.save()
        context = {
            'current': state.current
        }
        return render(request, 'business.html', context)

class Login(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,"Login Failed. Please try again.")
            # Return an 'invalid login' error message.
            print("Fel password " + request.POST.get('password'))
            print("Fel username " + request.POST.get('username'))
            return render(request, 'login.html')
       

class Register(View):  
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        businessName = request.POST['businessName']
        owner = request.POST['owner']
        passwordOne = request.POST['passwordOne']
        passwordTwo = request.POST['passwordTwo']
        user = authenticate(request, username=username, password=password)
        




class UserPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    # URL, for example: .../user?baronen
    def get(self, request, *args, **kwargs):
        businessName = request.get_full_path().split("?")[1]
        state = get_object_or_404(State, business__username = businessName)
        ticket = state.next
        if state.current > ticket:
            ticket = state.current 
        state.next = ticket +1
        state.save()
        return redirect('/usertwo?' + str(ticket) + "&" + businessName) # URL, for example: .../usertwo?46&Baronen


class UserTwoPage(View):
    model = State

    # URL, for example: .../usertwo?46&Baronen
    def get(self, request, *args, **kwargs):
        url = request.get_full_path() # ".../usertwo?46&Baronen"
        parts = url.split("?") # [".../usertwo", "46&Baronen"]
        queryString = parts[1] # 46&Baronen
        partstwo = queryString.split("&")      # ["46", "Baronen"]
        ticket = partstwo[0]      # 46
        businessName = partstwo[1]     # Baronen
        state = get_object_or_404(State, business__username = businessName)
        context = {
            'current': state.current,
            'ticket': ticket,
            'remaining': int(ticket) - state.current,
        }
        return render(request, 'user.html', context)
