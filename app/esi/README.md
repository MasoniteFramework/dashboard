# EVE Online ESI Integration

This directory contains the EVE Online ESI (EVE Swagger Interface) API integration with automatic OAuth2 token refresh.

## Features

✅ **Automatic Token Refresh** - Tokens are automatically refreshed when expired  
✅ **JWT Decoding** - Automatically detects token expiration time  
✅ **Proactive Refresh** - Refreshes tokens 60 seconds before expiry  
✅ **Error Handling** - Automatic retry with token refresh on 401 errors  
✅ **Public & Authenticated Endpoints** - Support for both public and authenticated API calls  

## Files

- **`ESIClient.py`** - Core ESI API client with OAuth2 token management
- **`User.py`** - Character/User API wrapper with convenience methods

## Quick Start

### 1. Set Up Authentication

Follow the guide in [`EVE_AUTH_SETUP.md`](../../EVE_AUTH_SETUP.md) to:
1. Create an EVE application
2. Get your CLIENT_ID and CLIENT_SECRET
3. Exchange authorization code for tokens

Or use the helper script:

```bash
python scripts/get_eve_tokens.py
```

### 2. Configure Environment

Add to your `.env` file:

```env
EVE_CLIENT_ID=your_client_id
EVE_CLIENT_SECRET=your_client_secret
EVE_ACCESS_TOKEN=your_access_token
EVE_REFRESH_TOKEN=your_refresh_token
```

### 3. Use in Your Code

```python
from app.esi.User import User

# Create user instance
user = User()

# Public endpoint (no auth required)
character = user.get_character(291969501)
print(f"Character: {character['name']}")

# Authenticated endpoint (auto-refreshes token if needed)
contacts = user.get_character_contacts(291969501)
print(f"Contacts: {len(contacts)}")
```

## How Token Refresh Works

```
┌─────────────────────────────────────────────────────────┐
│  Request Made                                           │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  Is Token Expired? (Check JWT expiry - 60s buffer)     │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼ YES               ▼ NO
┌───────────────┐    ┌──────────────┐
│ Refresh Token │    │ Make Request │
└───────┬───────┘    └──────┬───────┘
        │                   │
        ▼                   ▼
┌───────────────┐    ┌──────────────┐
│ Update Tokens │    │ Return Data  │
└───────┬───────┘    └──────────────┘
        │
        ▼
┌───────────────┐
│ Make Request  │
└───────┬───────┘
        │
        ▼
  ┌─────────────┐
  │ Got 401?    │
  └─────┬───────┘
        │
    ┌───┴───┐
    │       │
    ▼ YES   ▼ NO
  ┌──────┐ ┌────────┐
  │Retry │ │Success │
  │Once  │ └────────┘
  └──────┘
```

## Available Methods

### ESIClient (Low-level)

```python
from app.esi.ESIClient import get_esi_client

client = get_esi_client()

# Set tokens (usually done automatically from config)
client.set_tokens(access_token, refresh_token, expires_in)

# Make requests
response = client.get("/latest/characters/123/", authenticated=True)
response = client.post("/latest/characters/123/contacts/", authenticated=True, json=data)
```

### User (High-level)

```python
from app.esi.User import User

user = User()

# Public Methods (No Auth)
character = user.get_character(character_id)
portrait_url = user.get_character_portrait(character_id, size=256)

# Authenticated Methods (Auto Token Refresh)
contacts = user.get_character_contacts(character_id)
standings = user.get_character_standings(character_id)
loyalty = user.get_character_loyalty_points(character_id)
medals = user.get_character_medals(character_id)

# Token Verification
token_info = user.verify_token()
```

## Error Handling

The system handles errors gracefully:

```python
# Invalid/Expired Token
try:
    user = User()
    contacts = user.get_character_contacts(123)
except Exception as e:
    print(f"Error: {e}")
    # System automatically attempts token refresh
```

## Configuration

All configuration is in `config/eve.py`:

- **OAuth2 Settings** - CLIENT_ID, CLIENT_SECRET, CALLBACK_URL
- **Token Storage** - ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_EXPIRY
- **ESI Settings** - Base URL, version, datasource
- **Scopes** - List of required OAuth2 scopes
- **Static Data** - Race, Bloodline, Ancestry mappings

## Security Notes

⚠️ **Important:**

1. Never commit tokens to version control
2. Use environment variables for sensitive data
3. Implement proper token storage (database) in production
4. Use HTTPS in production
5. Rotate tokens regularly

## Extending

To add new ESI endpoints:

```python
# In User.py
def get_character_wallet(self, character_id):
    """Get character wallet balance"""
    response = self.client.get(
        f"/latest/characters/{character_id}/wallet/",
        authenticated=True
    )
    if response.status_code == 200:
        return response.json()
    return None
```

## Troubleshooting

### Token Refresh Fails
- Check that CLIENT_ID and CLIENT_SECRET are correct
- Verify REFRESH_TOKEN is still valid
- Re-authenticate if refresh token is expired/revoked

### 401 Errors Persist
- Token may be invalid for the requested scope
- Check that required scopes are included in your application
- Re-authenticate with correct scopes

### No Response / Timeout
- Check network connectivity
- Verify ESI service status: https://status.eveonline.com/

## Resources

- [EVE ESI Documentation](https://esi.evetech.net/ui/)
- [EVE Developer Portal](https://developers.eveonline.com/)
- [OAuth2 Guide](https://docs.esi.evetech.net/docs/sso/)
- [EVE Third Party Developer Documentation](https://docs.esi.evetech.net/)

