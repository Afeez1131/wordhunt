from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)


def login_user(request):
    next = request.GET.get('next')
    logger.info('checking to see if we have next in the URLS kwargs: {}'.format(str(next)))
    if request.method == 'POST':
        logger.info('posted DATA: ', request.POST)
        logger.info(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('core:home'))
            else:
                logger.warning('not active user')
                messages.error(request, 'User not Active')
        else:
            logger.warning('invalid username and or password')
            messages.error(request, 'Incorrect Username and/or Password.')
    return render(request, 'account/login.html')


def logout_user(request):
    logger.warning('logging out user')
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))
