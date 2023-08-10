from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser, User


@database_sync_to_async
def get_user(user_id):
    if user_id:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
    else:
        return None


class QueryAuthentication:
    """
    takes user id as query params
    :param ?user_id
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        uid = scope.get('query_string')
        user = await get_user(uid)
        if user:
            scope['user'] = user
        return await self.app(scope, receive, send)
