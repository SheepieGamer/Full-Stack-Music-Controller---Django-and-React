from django.shortcuts import redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import update_or_create_user_tokens


class AuthURL(APIView):
    def get(self, request: Request, format=None) -> Response:
        """
        Returns a URL to authenticate the user with Spotify.

        Args:
            request (Request): The incoming request.
            format (str): The format of the request.

        Returns:
            Response: A response containing the authentication URL.
        """
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

        url = Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "scope": scopes,
                "response_type": "code",
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
            },
        ).prepare().url

        return Response({"url": url}, status=status.HTTP_200_OK)
    
def spotify_callback(request: Request, format=None) -> Response:
    """
    This function is triggered when the user visits the /spotify/callback endpoint.
    It exchanges the authorization code for an access token and stores it in the user's session.
    Args:
        request (Request): The incoming request.
        format (str): The format of the request.
    Returns:
        Response: A redirect response to the frontend room page.
    """
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get("refresh_token")
    expires_in = response.get("expires_in")
    error = response.get("error")

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:room')