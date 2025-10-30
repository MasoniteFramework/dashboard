from masonite.environment import env

# EVE Online OAuth2 Configuration
CLIENT_ID = env("EVE_CLIENT_ID", "")
CLIENT_SECRET = env("EVE_CLIENT_SECRET", "")
CALLBACK_URL = env("EVE_CALLBACK_URL", "http://localhost:8000/auth/eve/callback")

# OAuth2 Token Storage (will be stored in database in production)
ACCESS_TOKEN = env("EVE_ACCESS_TOKEN", "")
REFRESH_TOKEN = env("EVE_REFRESH_TOKEN", "")
TOKEN_EXPIRY = env("EVE_TOKEN_EXPIRY", 0)

# EVE ESI Configuration
ESI_BASE_URL = "https://esi.evetech.net"
ESI_VERSION = "latest"
ESI_DATASOURCE = "tranquility"

# OAuth2 URLs
OAUTH_AUTHORIZE_URL = "https://login.eveonline.com/v2/oauth/authorize"
OAUTH_TOKEN_URL = "https://login.eveonline.com/v2/oauth/token"
OAUTH_VERIFY_URL = "https://esi.evetech.net/verify/"

# Scopes required
OAUTH_SCOPES = [
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

# EVE Race Mapping
RACE = {
    "1": "Caldari",
    "2": "Minmatar",
    "3": "Amarr",
    "4": "Gallente",
}

FACTION = {
    "1": "Caldari",
    "2": "Minmatar",
    "3": "Amarr",
    "4": "Gallente",
}

INDUSTRY_ACTIVITY = {
    1: "Manufacturing",
    2: "Researching Technology",
    3: "Researching Materials",
    4: "Copying",
    5: "Invention",
    6: "Reverse Engineering",
}

# EVE Bloodline Mapping
BLOODLINE = {
    "1": "Deteis",
    "2": "Civire",
    "3": "Sebiestor",
    "4": "Brutor",
    "5": "Amarr",
    "6": "Ni-Kunni",
    "7": "Gallente",
    "8": "Intaki",
    "9": "Achura",
    "10": "Jin-Mei",
    "11": "Khanid",
    "12": "Vherokior",
    "13": "Drifter",
    "14": "Static",
}

# EVE Ancestry Mapping (simplified)
ANCESTRY = {
    "1": "Liberal Holders",
    "2": "Wealthy Commoners",
    "3": "Religious Reclaimers",
    "4": "Free Merchants",
    "5": "Border Runners",
    "6": "Navy Veterans",
    "7": "Cyber Knights",
    "8": "Unionists",
    "9": "Entrepeneurs",
    "10": "Mercs",
    "11": "Dissenters",
    "12": "Merchandisers",
    "13": "Scientists",
    "14": "Tube Child",
    "15": "Tinkers",
    "16": "Traders",
    "17": "Rebels",
    "18": "Workers",
    "19": "Tribal Traditionalists",
    "20": "Slave Child",
    "21": "Elders",
    "22": "Unsullied",
    "23": "Starkmanir",
    "24": "Activists",
    "25": "Miners",
    "26": "Immigrants",
    "27": "Artists",
    "28": "Diplomats",
    "29": "Reborn",
    "30": "Sang Do Caste",
    "31": "Saan Go Caste",
    "32": "Jing Ko Caste",
    "33": "Inventors",
    "34": "Monks",
    "35": "Stargazers",
    "36": "Zealots",
    "37": "Cyber Knights",
    "38": "Shakorite",
    "39": "Drifter",
    "40": "Static",
}