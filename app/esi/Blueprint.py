from app.esi.ESIClient import get_esi_client
import requests


class Blueprint:
    """
    EVE Online Blueprint API wrapper with automatic token refresh
    """
    
    def __init__(self):
        self.client = get_esi_client()
        self._type_cache = {}  # Cache for type information
        self._category_cache = {}  # Cache for category information
        self._group_cache = {}  # Cache for group information
    
    def get_character_blueprints(self, character_id):
        """
        Get character blueprints (requires authentication and esi-characters.read_blueprints.v1 scope)
        
        Args:
            character_id: EVE character ID
            
        Returns:
            list: Character blueprints with enriched data
        """
        response = self.client.get(
            f"/latest/characters/{character_id}/blueprints/",
            authenticated=True
        )
        
        if response.status_code == 200:
            blueprints = response.json()
            
            # Enrich blueprints with type information
            enriched_blueprints = []
            for bp in blueprints:
                enriched_bp = self._enrich_blueprint(bp)
                if enriched_bp:
                    enriched_blueprints.append(enriched_bp)
            
            return enriched_blueprints
        else:
            print(f"Error fetching blueprints: {response.status_code} - {response.text}")
            return []
    
    def _enrich_blueprint(self, blueprint):
        """
        Enrich blueprint data with type, category, and group information
        
        Args:
            blueprint: Blueprint data from ESI
            
        Returns:
            dict: Enriched blueprint data
        """
        type_id = blueprint.get('type_id')
        if not type_id:
            return None
        
        # Get type information
        type_info = self._get_type_info(type_id)
        if not type_info:
            return None
        
        # Get group information
        group_id = type_info.get('group_id')
        group_info = self._get_group_info(group_id) if group_id else {}
        
        # Get category information
        category_id = group_info.get('category_id')
        category_info = self._get_category_info(category_id) if category_id else {}
        
        # Build enriched blueprint
        enriched = {
            'item_id': blueprint.get('item_id'),
            'type_id': type_id,
            'type_name': type_info.get('name', 'Unknown'),
            'location_id': blueprint.get('location_id'),
            'location_flag': blueprint.get('location_flag', 'Unknown'),
            'quantity': blueprint.get('quantity', -1),
            'time_efficiency': blueprint.get('time_efficiency', 0),
            'material_efficiency': blueprint.get('material_efficiency', 0),
            'runs': blueprint.get('runs', -1),
            'category': category_info.get('name', 'Unknown'),
            'category_id': category_id,
            'group': group_info.get('name', 'Unknown'),
            'group_id': group_id,
        }
        
        return enriched
    
    def _get_type_info(self, type_id):
        """
        Get type information from ESI with caching
        
        Args:
            type_id: EVE type ID
            
        Returns:
            dict: Type information
        """
        if type_id in self._type_cache:
            return self._type_cache[type_id]
        
        response = self.client.get(f"/latest/universe/types/{type_id}/")
        
        if response.status_code == 200:
            type_info = response.json()
            self._type_cache[type_id] = type_info
            return type_info
        else:
            print(f"Error fetching type {type_id}: {response.status_code}")
            return None
    
    def _get_group_info(self, group_id):
        """
        Get group information from ESI with caching
        
        Args:
            group_id: EVE group ID
            
        Returns:
            dict: Group information
        """
        if group_id in self._group_cache:
            return self._group_cache[group_id]
        
        response = self.client.get(f"/latest/universe/groups/{group_id}/")
        
        if response.status_code == 200:
            group_info = response.json()
            self._group_cache[group_id] = group_info
            return group_info
        else:
            print(f"Error fetching group {group_id}: {response.status_code}")
            return {}
    
    def _get_category_info(self, category_id):
        """
        Get category information from ESI with caching
        
        Args:
            category_id: EVE category ID
            
        Returns:
            dict: Category information
        """
        if category_id in self._category_cache:
            return self._category_cache[category_id]
        
        response = self.client.get(f"/latest/universe/categories/{category_id}/")
        
        if response.status_code == 200:
            category_info = response.json()
            self._category_cache[category_id] = category_info
            return category_info
        else:
            print(f"Error fetching category {category_id}: {response.status_code}")
            return {}
    
    def get_blueprint_details(self, type_id):
        """
        Get detailed blueprint information including materials and activities
        
        Args:
            type_id: Blueprint type ID
            
        Returns:
            dict: Blueprint details with materials and activities
        """
        # Get type info
        type_info = self._get_type_info(type_id)
        if not type_info:
            return None
        
        # ESI doesn't have a specific blueprint details endpoint
        # but we can get basic info from the type endpoint
        return {
            'type_id': type_id,
            'name': type_info.get('name'),
            'description': type_info.get('description'),
            'published': type_info.get('published'),
            'group_id': type_info.get('group_id'),
        }

