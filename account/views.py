from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login_user(request):
    next = request.GET.get('next')
    print('next: ', next)
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'User not Active')
        else:
            messages.error(request, 'Incorrect Username and/or Password.')
    return render(request, 'account/login.html')
