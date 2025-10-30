from masonite.configuration import config
import base64
import requests
from masonite.facades import Request

class SSO:

    def get_authorize_url(self, client_id: str, redirect_uri: str, state: str) -> str:
        return f"https://login.eveonline.com/v2/oauth/authorize?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}&state={state}"
    
    def authorization_header_code(self) -> str:
        eve_client = config("eve.client_id")
        eve_secret = config("eve.client_secret")
        base_64_encoded = f"{eve_client}:{eve_secret}"
        base_64_encoded = base64.b64encode(base_64_encoded.encode()).decode()
        return base_64_encoded
    
    def token_is_expired(self) -> bool:
        """Check if the current access token is expired"""
        expiry = Request.cookie("eve_access_token_expires")
        if not expiry:
            return True
        import pendulum
        expiry_time = pendulum.parse(expiry)
        return pendulum.now() >= expiry_time
    
    def get_access_token(self, token, refresh_token=None) -> str:
        """Get the current access token"""

        

        if self.token_is_expired() and token:
            refreshed = self.refresh_token(refresh_token)
            token = refreshed.get("access_token", None)
        if token:
            self.access_token = token

        return token
    
    def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        eve_response = requests.post("https://login.eveonline.com/v2/oauth/token", data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8000/auth/eve/callback",
            }, 
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + self.authorization_header_code()
            })
        
        if eve_response.status_code == 200:
            return eve_response.json()
        else:
            raise Exception(f"Failed to exchange code for token: {eve_response.status_code} - {eve_response.text}")

    def refresh_token(self, refresh_token: str) -> dict:
        eve_response = requests.post("https://login.eveonline.com/v2/oauth/token", data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            }, 
            headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + self.authorization_header_code()
        })

        if eve_response.status_code == 200:
            return eve_response.json()
        else:
            raise Exception(f"Failed to exchange code for token: {eve_response.status_code} - {eve_response.text}")