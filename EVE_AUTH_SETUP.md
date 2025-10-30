# EVE Online OAuth2 Setup Guide

This guide will help you set up OAuth2 authentication for your EVE Online character dashboard.

## Step 1: Create an EVE Application

1. Go to [EVE Developers](https://developers.eveonline.com/)
2. Log in with your EVE Online account
3. Go to "Manage Applications"
4. Click "Create New Application"
5. Fill in the details:
   - **Application Name**: Your Dashboard Name
   - **Description**: Character Dashboard
   - **Connection Type**: Authentication & API Access
   - **Permissions**: Select the scopes you need (already configured in `config/eve.py`)
   - **Callback URL**: `http://localhost:8000/auth/eve/callback`

6. Click "Create Application"
7. Save your **Client ID** and **Client Secret**

## Step 2: Configure Environment Variables

Create or edit your `.env` file in the project root:

```env
# EVE Online OAuth2
EVE_CLIENT_ID=your_client_id_here
EVE_CLIENT_SECRET=your_client_secret_here
EVE_CALLBACK_URL=http://localhost:8000/auth/eve/callback

# These will be set after authentication
EVE_ACCESS_TOKEN=
EVE_REFRESH_TOKEN=
EVE_TOKEN_EXPIRY=0
```

## Step 3: Get Your Tokens

### Option A: Manual Token Generation (Quick Start)

1. Build the authorization URL:
   ```
   https://login.eveonline.com/v2/oauth/authorize?response_type=code&redirect_uri=http://localhost:8000/auth/eve/callback&client_id=YOUR_CLIENT_ID&scope=esi-characters.read_contacts.v1 esi-characters.write_contacts.v1 esi-characters.read_loyalty.v1 esi-characters.read_medals.v1 esi-characters.read_standings.v1 esi-characters.read_agents_research.v1 esi-characters.read_blueprints.v1 esi-characters.read_corporation_roles.v1 esi-characters.read_fatigue.v1 esi-characters.read_notifications.v1 esi-characters.read_titles.v1 esi-characters.read_fw_stats.v1
   ```

2. Visit this URL in your browser and authorize
3. You'll be redirected to your callback URL with a `code` parameter
4. Use this code to get your tokens (see below)

### Option B: Using the Token Exchange Script

Run the included token exchange helper:

```bash
python scripts/get_eve_tokens.py
```

Follow the prompts to:
1. Authorize your application
2. Get the authorization code from the redirect URL
3. Exchange it for access and refresh tokens

## Step 4: Exchange Authorization Code for Tokens

Once you have an authorization code, exchange it for tokens:

```python
import requests
import base64

client_id = "your_client_id"
client_secret = "your_client_secret"
auth_code = "authorization_code_from_callback"
callback_url = "http://localhost:8000/auth/eve/callback"

# Create basic auth header
auth_string = f"{client_id}:{client_secret}"
auth_bytes = base64.b64encode(auth_string.encode('ascii'))
auth_b64 = auth_bytes.decode('ascii')

headers = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": callback_url,
}

response = requests.post(
    "https://login.eveonline.com/v2/oauth/token",
    headers=headers,
    data=data
)

if response.status_code == 200:
    tokens = response.json()
    print(f"Access Token: {tokens['access_token']}")
    print(f"Refresh Token: {tokens['refresh_token']}")
    print(f"Expires In: {tokens['expires_in']} seconds")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Step 5: Update Your .env File

Add the tokens to your `.env` file:

```env
EVE_ACCESS_TOKEN=your_access_token_here
EVE_REFRESH_TOKEN=your_refresh_token_here
```

## How It Works

Once configured, the system will:

1. **Automatic Token Refresh**: When the access token expires (typically after 20 minutes), the system automatically uses the refresh token to get a new access token
2. **JWT Decoding**: The system decodes the JWT access token to know exactly when it expires
3. **Proactive Refresh**: Tokens are refreshed 60 seconds before they expire to prevent API errors
4. **Error Handling**: If a 401 error is received, the system attempts one token refresh before failing

## Token Refresh Flow

```
1. Request made → Check if token expired
2. If expired → Use refresh_token to get new access_token
3. Update tokens → Make the original request
4. If 401 received → Refresh once more and retry
```

## Testing Your Setup

Test that authentication works:

```python
from app.esi.User import User

user = User()

# Test token verification
token_info = user.verify_token()
print(f"Authenticated as: {token_info}")

# Test fetching character data (public - no auth needed)
character = user.get_character(291969501)
print(f"Character: {character['name']}")

# Test fetching authenticated data
contacts = user.get_character_contacts(291969501)
print(f"Found {len(contacts)} contacts")
```

## Scopes Currently Configured

The following scopes are configured in `config/eve.py`:

- `esi-characters.read_contacts.v1` - Read character contacts
- `esi-characters.write_contacts.v1` - Modify character contacts
- `esi-characters.read_loyalty.v1` - Read loyalty points
- `esi-characters.read_medals.v1` - Read medals
- `esi-characters.read_standings.v1` - Read standings
- `esi-characters.read_agents_research.v1` - Read agent research
- `esi-characters.read_blueprints.v1` - Read blueprints
- `esi-characters.read_corporation_roles.v1` - Read corporation roles
- `esi-characters.read_fatigue.v1` - Read jump fatigue
- `esi-characters.read_notifications.v1` - Read notifications
- `esi-characters.read_titles.v1` - Read titles
- `esi-characters.read_fw_stats.v1` - Read faction warfare stats

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit tokens to git** - Add `.env` to `.gitignore`
2. **Refresh tokens are long-lived** - They can be used until revoked
3. **Store tokens securely** - In production, use a database or secure vault
4. **Rotate tokens regularly** - Implement token rotation in production
5. **Use HTTPS in production** - Never send tokens over HTTP

## Troubleshooting

### "No refresh token available"
- You haven't set up authentication yet
- Follow steps 1-5 above

### "Failed to refresh token: 400"
- Your refresh token is invalid or expired
- Re-authenticate using steps 3-5

### "EVE_CLIENT_ID and EVE_CLIENT_SECRET must be set"
- Check your `.env` file has these values
- Restart your application after updating `.env`

### Token keeps expiring
- This is normal! Access tokens expire after 20 minutes
- The system automatically refreshes them using the refresh token
- If refresh token is invalid, you need to re-authenticate

## Next Steps

1. Set up proper database storage for tokens (recommended for production)
2. Implement OAuth2 callback route to automate token exchange
3. Add token refresh status to your dashboard UI
4. Implement multi-character support with separate token storage per character

