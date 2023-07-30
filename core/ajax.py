from datetime import datetime, timezone

from django.http import JsonResponse

from core.models import GameRoom


def ajax_create_game(request):
    try:
        recent_game = GameRoom.objects.filter(creator=request.user).latest()
        now = datetime.now(timezone.utc)
        time_diff = (now - recent_game.created).days
        if time_diff >= 1:
            game = GameRoom.objects.create(creator=request.user)
        else:
            game = recent_game
        invitation_text = f'''📢 Attention all wordsmiths! We're hosting a game of Word Challenge on Word Warrior Game Room. Join now using the code Code: ({game.lobby.shortcode}) and let the wordplay begin! 🚀🔠'''
        return JsonResponse({'status': 'success',
                             'invitation': invitation_text})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})

