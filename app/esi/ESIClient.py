import requests
import base64
import time
import json
from datetime import datetime, timedelta
from masonite.facades import Config


class ESIClient:
    """
    EVE Online ESI API Client with automatic token refresh
    """
    
    def __init__(self):
        self.client_id = Config.get("eve.client_id")
        self.client_secret = Config.get("eve.client_secret")
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0
        self.base_url = Config.get("eve.esi_base_url")
        self.oauth_token_url = Config.get("eve.oauth_token_url")
        
    def set_tokens(self, access_token, refresh_token, expires_in=1200):
        """Set the OAuth2 tokens"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = time.time() + expires_in
        
    def is_token_expired(self):
        """Check if the access token is expired or about to expire (within 60 seconds)"""
        if not self.access_token:
            return True
        return time.time() >= (self.token_expiry - 60)
    
    def decode_jwt(self, token):
        """Decode JWT token to get expiry time"""
        try:
            # Split the JWT token
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            # Decode the payload (second part)
            payload = parts[1]
            # Add padding if necessary
            padding = len(payload) % 4
            if padding:
                payload += '=' * (4 - padding)
            
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
        except Exception as e:
            print(f"Error decoding JWT: {e}")
            return None
    
    def refresh_access_token(self):
        """Refresh the access token using the refresh token"""
        if not self.refresh_token:
            raise Exception("No refresh token available. Please authenticate first.")
        
        if not self.client_id or not self.client_secret:
            raise Exception("EVE_CLIENT_ID and EVE_CLIENT_SECRET must be set in config/eve.py or .env")
        
        # Prepare authentication
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        try:
            response = requests.post(self.oauth_token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                self.refresh_token = token_data.get('refresh_token', self.refresh_token)
                expires_in = token_data.get('expires_in', 1200)
                self.token_expiry = time.time() + expires_in
                
                print(f"✓ Token refreshed successfully. Expires in {expires_in} seconds.")
                return True
            else:
                error_msg = f"Failed to refresh token: {response.status_code} - {response.text}"
                print(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            print(f"Error refreshing token: {e}")
            raise
    
    def ensure_valid_token(self):
        """Ensure we have a valid access token, refresh if necessary"""
        if self.is_token_expired():
            print("Token expired or about to expire, refreshing...")
            self.refresh_access_token()
    
    def make_request(self, method, endpoint, authenticated=False, **kwargs):
        """
        Make a request to ESI API with automatic token refresh
        
        Args:
            method: HTTP method (get, post, put, delete)
            endpoint: API endpoint (e.g., '/characters/123/')
            authenticated: Whether this endpoint requires authentication
            **kwargs: Additional arguments to pass to requests
        """
        # Ensure token is valid if authentication is required
        if authenticated:
            self.ensure_valid_token()
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers']['Authorization'] = f"Bearer {self.access_token}"
        
        # Build full URL
        if not endpoint.startswith('http'):
            url = f"{self.base_url}{endpoint}"
        else:
            url = endpoint
        
        # Make request
        try:
            response = requests.request(method, url, **kwargs)
            
            # If we get 401 and we're authenticated, try to refresh token once
            if response.status_code == 401 and authenticated:
                print("Received 401, attempting token refresh...")
                self.refresh_access_token()
                kwargs['headers']['Authorization'] = f"Bearer {self.access_token}"
                response = requests.request(method, url, **kwargs)
            
            return response
            
        except Exception as e:
            print(f"Error making request to {url}: {e}")
            raise
    
    def get(self, endpoint, authenticated=False, **kwargs):
        """Make a GET request"""
        return self.make_request('get', endpoint, authenticated, **kwargs)
    
    def post(self, endpoint, authenticated=False, **kwargs):
        """Make a POST request"""
        return self.make_request('post', endpoint, authenticated, **kwargs)
    
    def put(self, endpoint, authenticated=False, **kwargs):
        """Make a PUT request"""
        return self.make_request('put', endpoint, authenticated, **kwargs)
    
    def delete(self, endpoint, authenticated=False, **kwargs):
        """Make a DELETE request"""
        return self.make_request('delete', endpoint, authenticated, **kwargs)
    
    def verify_token(self):
        """Verify the current access token and get character info"""
        if not self.access_token:
            return None
        
        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = requests.get(Config.get("eve.OAUTH_VERIFY_URL"), headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error verifying token: {e}")
            return None


# Singleton instance
_esi_client = None


def get_esi_client():
    """Get or create the ESI client singleton"""
    global _esi_client
    if _esi_client is None:
        _esi_client = ESIClient()
        
        # Try to load tokens from config
        access_token = Config.get("eve.ACCESS_TOKEN")
        refresh_token = Config.get("eve.REFRESH_TOKEN")
        
        if access_token and refresh_token:
            # Decode JWT to get expiry
            client = _esi_client
            jwt_data = client.decode_jwt(access_token)
            if jwt_data and 'exp' in jwt_data:
                expires_in = jwt_data['exp'] - time.time()
                if expires_in > 0:
                    client.set_tokens(access_token, refresh_token, int(expires_in))
                else:
                    # Token already expired, set it anyway and let refresh handle it
                    client.set_tokens(access_token, refresh_token, 0)
            else:
                # Couldn't decode, assume default expiry
                client.set_tokens(access_token, refresh_token)
    
    return _esi_client

