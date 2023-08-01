from django.contrib.auth import get_user_model, authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


def ajax_login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    next = request.POST.get('next')
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'status': 'success', 'next': next})
        else:
            return JsonResponse({'status': 'error', 'error': 'Invalid Username or Password'})
    else:
        return JsonResponse({'status': 'error', 'error': f'User with the Username {username} does not exist.'})


def ajax_register_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm-password')
    next = request.POST.get('next')
    if password != confirm_password:
        logger.info('Password not the same')
        return JsonResponse({'status': 'error', 'error': 'Password not the same.'})
    if User.objects.filter(username=username).exists():
        logger.info(f'user with username {username} exist')
        return JsonResponse({'status': 'error', 'error': 'User with this Username already exist.'})
    try:
        user = User.objects.create_user(username=username, password=password)
        user = authenticate(request, username=username, password=password)
        login(request, user)
        logger.info('Logged in User')
        return JsonResponse({'status': 'success', 'next': next})
    except Exception as e:
        logger.info('Exception error: {}'.format(e))
        return JsonResponse({'status': 'error', 'error': str(e), 'next': next})
