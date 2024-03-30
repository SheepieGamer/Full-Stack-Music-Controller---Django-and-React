from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from typing import Optional

def get_user_tokens(session_id: str) -> Optional[SpotifyToken]:
    """
    Get the user's Spotify access and refresh tokens.

    Args:
        session_id (str): The user's session ID.

    Returns:
        Optional[SpotifyToken]: The user's Spotify access and refresh tokens, or None if they do not exist.
    """
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    return None

def update_or_create_user_tokens(session_id: str, access_token: str, token_type: str, expires_in: int, refresh_token: str) -> None:
    """
    Update or create the user's Spotify access and refresh tokens.

    Args:
        session_id (str): The user's session ID.
        access_token (str): The user's access token.
        token_type (str): The type of token.
        expires_in (int): The number of seconds until the token expires.
        refresh_token (str): The user's refresh token.

    Returns:
        None

    """
    tokens = get_user_tokens(session_id=session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()