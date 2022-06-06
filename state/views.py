from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from .models import State
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


@method_decorator(login_required, name='get')
class ControlPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    def get(self, request, *args, **kwargs):
        state = get_object_or_404(State, business=request.user)
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
        # URL, for example: .../user?baronen
        url = 'https://8000-emmabergner-dontq-zj38f323g5o.ws-eu46.gitpod.io'

        url_pop_up_text = f"{url}/user?{state.business}"
        opentext = f"Helping currently now:"
        if state.current == 0:
            opentext = f"Press the green button to start the queue."
        context = {
            'text': opentext,
            'current': state.current,
            'userurl': f"functionAlert('{url_pop_up_text}')",
            'businessname': state.business
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
            messages.error(request, "Login Failed. Please try again.")
            # Return an 'invalid login' error message.
            print("Fel password " + request.POST.get('password'))
            print("Fel username " + request.POST.get('username'))
            return render(request, 'login.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        businessName = request.POST['businessName']
        email = request.POST['owner']
        passwordOne = request.POST['passwordOne']
        passwordTwo = request.POST['passwordTwo']
        # Check password match and business does exist.
        if User.objects.filter(username=businessName).exists():
            messages.error(
                request, "Business does already exist. Please log in.")
            return render(request, 'register.html')
        if not passwordOne == passwordTwo:
            messages.error(
                request, "Password does not match. Please try again.")
            return render(request, 'register.html')
        user = User.objects.create_user(username=businessName,
                                        password=passwordOne,
                                        email=email)
        State.objects.create(business=user)
        logout(request)
        return redirect('/')

 
class Update(View):
    def get(self, request, *args, **kwargs):
        if (request.GET.get('delete')):
            user = User.objects.get(username=request.user.username)
            user.delete()
            return redirect('/')
        return render(request, 'update.html', makeUpdateContext(request.user))

    def post(self, request, *args, **kwargs):
        email = request.POST['owner']
        passwordOne = request.POST['passwordOne']
        passwordTwo = request.POST['passwordTwo']
        # Check password match and business does exist.
        if not passwordOne == passwordTwo:
            messages.error(
                request, "Password does not match. Please try again.")
            return render(request, 'update.html')
        # User.objects.update_user(username=businessName, email=email)
        u =request.user
        u.email = email
        u.save()
        # p = request.user
        # p.password = password
        # p.save()
        return redirect('/')
 

def makeUpdateContext(user):
    return {'businessName': user.username, 'contactEmail' : user.email}


class UserPage(View):
    model = State
    template_name = 'business.html'
    template_name = 'user.html'

    # URL, for example: .../user?baronen
    def get(self, request, *args, **kwargs):
        businessName = request.get_full_path().split("?")[1]
        state = get_object_or_404(State, business__username=businessName)
        ticket = state.next
        if state.current > ticket:
            ticket = state.current
        state.next = ticket + 1
        state.save()
        # URL, for example: .../usertwo?46&Baronen
        return redirect('/usertwo?' + str(ticket) + "&" + businessName)


class UserTwoPage(View):
    model = State

    # URL, for example: .../usertwo?46&Baronen
    def get(self, request, *args, **kwargs):
        url = request.get_full_path()  # ".../usertwo?46&Baronen"
        parts = url.split("?")  # [".../usertwo", "46&Baronen"]
        queryString = parts[1]  # 46&Baronen
        partstwo = queryString.split("&")      # ["46", "Baronen"]
        ticket = partstwo[0]      # 46
        businessName = partstwo[1]     # Baronen
        state = get_object_or_404(State, business__username=businessName)
        context = makeContext(state.current, ticket)
        return render(request, 'user.html', context)


def makeContext(currentInt, ticket):
    ticketInt = int(ticket)
    if currentInt == ticketInt:
        return {'current': "", 'ticket': "It is your turn", 'remaining': ""}
    if ticketInt - currentInt < 0 : 
        return {'current': "", 'ticket': "You missed your turn", 'remaining': ""}
    current = f"We are helping number {currentInt}"
    ticketIntStr = str(ticketInt)
    if currentInt == 0:
        current = f"We are just about to open."
        ticketIntStr = ""
    ticketText = f"Your number is:"
    ticket = f"{ticketInt} "
    remaining = f"So {ticketInt - currentInt} are in line before you."
    return {'current': current, 'ticketText' : ticketText, 'ticket': ticketIntStr, 'remaining': remaining}


