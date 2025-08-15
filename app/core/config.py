import os
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# Google OAuth2 Client Config
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),    # Set your Google client ID in env
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),    # Set your Google client secret in env
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    authorize_params=None,
    client_kwargs={'scope': 'openid profile email'},
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is Google’s OpenID user info endpoint
)
