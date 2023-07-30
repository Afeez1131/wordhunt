from django.contrib.auth import get_user_model, authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse

User = get_user_model()


def ajax_login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return JsonResponse({'status': 'success'})
    else:
        try:
            User.objects.create_user(username=username, password=password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error', 'error': 'Error occured.'})
