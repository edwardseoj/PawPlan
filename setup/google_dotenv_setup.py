import os
from dotenv import load_dotenv
from flet.auth.providers import GoogleOAuthProvider

load_dotenv()
client_id = os.getenv("GOOGLE_CLIENT_ID")
client_secret = os.getenv("GOOGLE_CLIENT_SECRET")


# error checking
if not client_id or not client_secret:
    raise ValueError("Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env file")


# auth code
provider = GoogleOAuthProvider(
    client_id=client_id,
    client_secret=client_secret,
    redirect_url="http://localhost:8550/oauth_callback",
)
