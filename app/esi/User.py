from app.esi.ESIClient import get_esi_client


class User:
    """
    EVE Online User/Character API wrapper with automatic token refresh
    """
    
    def __init__(self):
        self.client = get_esi_client()
    
    def get_character(self, character_id):
        """
        Get public character information (no authentication required)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            dict: Character information
        """
        response = self.client.get(f"/latest/characters/{character_id}/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching character {character_id}: {response.status_code}")
            return None
    
    def get_character_portrait(self, character_id, size=256):
        """
        Get character portrait URL
        
        Args:
            character_id: EVE character ID
            size: Image size (64, 128, 256, 512, 1024)
            
        Returns:
            str: Portrait URL
        """
        return f"https://images.evetech.net/characters/{character_id}/portrait?size={size}"
    
    def get_character_contacts(self, character_id):
        """
        Get character contacts (requires authentication)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            list: Character contacts
        """
        response = self.client.get(
            f"/latest/characters/{character_id}/contacts/",
            authenticated=True
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching contacts: {response.status_code}")
            return []
    
    def get_character_standings(self, character_id):
        """
        Get character standings (requires authentication)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            list: Character standings
        """
        response = self.client.get(
            f"/latest/characters/{character_id}/standings/",
            authenticated=True
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching standings: {response.status_code}")
            return []
    
    def get_character_loyalty_points(self, character_id):
        """
        Get character loyalty points (requires authentication)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            list: Character loyalty points
        """
        response = self.client.get(
            f"/latest/characters/{character_id}/loyalty/points/",
            authenticated=True
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching loyalty points: {response.status_code}")
            return []
    
    def get_character_medals(self, character_id):
        """
        Get character medals (requires authentication)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            list: Character medals
        """
        response = self.client.get(
            f"/latest/characters/{character_id}/medals/",
            authenticated=True
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching medals: {response.status_code}")
            return []
    
    def verify_token(self):
        """
        Verify the current access token
        
        Returns:
            dict: Token verification info including character ID
        """
        return self.client.verify_token()
    
    # Alias for backward compatibility
    def get_user(self, user_id):
        """Backward compatibility method"""
        return self.get_character(user_id)