#!/usr/bin/env python3
"""
EVE Online OAuth2 Token Exchange Helper

This script helps you exchange an authorization code for access and refresh tokens.
"""

import requests
import base64
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from masonite.environment import LoadEnvironment

# Load environment
LoadEnvironment()


def get_authorization_url(client_id, callback_url, scopes):
    """Generate the authorization URL"""
    scope_string = " ".join(scopes)
    url = (
        f"https://login.eveonline.com/v2/oauth/authorize"
        f"?response_type=code"
        f"&redirect_uri={callback_url}"
        f"&client_id={client_id}"
        f"&scope={scope_string}"
        f"&state=unique_state_string"
    )
    return url


def exchange_code_for_tokens(client_id, client_secret, auth_code, callback_url):
    """Exchange authorization code for access and refresh tokens"""
    
    # Create basic auth header
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = base64.b64encode(auth_string.encode('ascii'))
    auth_b64 = auth_bytes.decode('ascii')
    
    headers = {
        "Authorization": f"Basic {auth_b64}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com",
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
    }
    
    try:
        response = requests.post(
            "https://login.eveonline.com/v2/oauth/token",
            headers=headers,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Error making request: {e}")
        return None


def main():
    print("=" * 70)
    print("EVE Online OAuth2 Token Exchange Helper")
    print("=" * 70)
    print()
    
    # Get configuration
    client_id = os.getenv("EVE_CLIENT_ID", "")
    client_secret = os.getenv("EVE_CLIENT_SECRET", "")
    callback_url = os.getenv("EVE_CALLBACK_URL", "http://localhost:8000/auth/eve/callback")
    
    if not client_id:
        client_id = input("Enter your EVE_CLIENT_ID: ").strip()
    else:
        print(f"✓ Using CLIENT_ID from .env: {client_id[:10]}...")
    
    if not client_secret:
        client_secret = input("Enter your EVE_CLIENT_SECRET: ").strip()
    else:
        print(f"✓ Using CLIENT_SECRET from .env: {client_secret[:10]}...")
    
    print(f"✓ Using CALLBACK_URL: {callback_url}")
    print()
    
    if not client_id or not client_secret:
        print("❌ Error: CLIENT_ID and CLIENT_SECRET are required!")
        print("\nPlease either:")
        print("1. Set them in your .env file")
        print("2. Enter them when prompted")
        sys.exit(1)
    
    # Scopes (from config)
    scopes = [
        "esi-characters.read_contacts.v1",
        "esi-characters.write_contacts.v1",
        "esi-characters.read_loyalty.v1",
        "esi-characters.read_medals.v1",
        "esi-characters.read_standings.v1",
        "esi-characters.read_agents_research.v1",
        "esi-characters.read_blueprints.v1",
        "esi-characters.read_corporation_roles.v1",
        "esi-characters.read_fatigue.v1",
        "esi-characters.read_notifications.v1",
        "esi-characters.read_titles.v1",
        "esi-characters.read_fw_stats.v1",
    ]
    
    # Generate authorization URL
    auth_url = get_authorization_url(client_id, callback_url, scopes)
    
    print("=" * 70)
    print("STEP 1: Authorize Your Application")
    print("=" * 70)
    print("\nVisit this URL in your browser:\n")
    print(auth_url)
    print("\n" + "=" * 70)
    print()
    
    print("After authorizing, you'll be redirected to your callback URL.")
    print("The URL will contain a 'code' parameter.")
    print()
    print("Example:")
    print("  http://localhost:8000/auth/eve/callback?code=ABC123XYZ&state=unique_state_string")
    print()
    
    # Get authorization code
    print("=" * 70)
    print("STEP 2: Enter Authorization Code")
    print("=" * 70)
    auth_code = input("\nPaste the 'code' parameter from the URL: ").strip()
    
    if not auth_code:
        print("\n❌ Error: No authorization code provided!")
        sys.exit(1)
    
    # Exchange code for tokens
    print("\n" + "=" * 70)
    print("STEP 3: Exchanging Code for Tokens")
    print("=" * 70)
    print("\n⏳ Exchanging authorization code...")
    
    tokens = exchange_code_for_tokens(client_id, client_secret, auth_code, callback_url)
    
    if tokens:
        print("\n✅ Success! Tokens received:")
        print("\n" + "=" * 70)
        print("Add these to your .env file:")
        print("=" * 70)
        print(f"\nEVE_ACCESS_TOKEN={tokens['access_token']}")
        print(f"EVE_REFRESH_TOKEN={tokens['refresh_token']}")
        print(f"\nToken expires in: {tokens.get('expires_in', 1200)} seconds (~{tokens.get('expires_in', 1200) // 60} minutes)")
        print("\n" + "=" * 70)
        
        # Verify token
        print("\n⏳ Verifying token...")
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        verify_response = requests.get("https://esi.evetech.net/verify/", headers=headers)
        
        if verify_response.status_code == 200:
            char_info = verify_response.json()
            print(f"\n✅ Token verified!")
            print(f"   Character: {char_info.get('CharacterName', 'Unknown')}")
            print(f"   Character ID: {char_info.get('CharacterID', 'Unknown')}")
            print(f"   Scopes: {len(char_info.get('Scopes', '').split())} scopes")
        else:
            print(f"\n⚠️  Token verification failed: {verify_response.status_code}")
        
        print("\n" + "=" * 70)
        print("🎉 Setup Complete!")
        print("=" * 70)
        print("\nYour application is now authenticated and ready to use!")
        print("The system will automatically refresh the token when it expires.")
        
    else:
        print("\n❌ Failed to exchange code for tokens.")
        print("\nPossible issues:")
        print("- Authorization code already used (codes can only be used once)")
        print("- Authorization code expired (codes expire after a few minutes)")
        print("- Incorrect CLIENT_ID or CLIENT_SECRET")
        print("- Network connection issues")
        print("\nPlease try again with a new authorization code.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

