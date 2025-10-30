from masonite.controllers import Controller
from masonite.views import View
from app.models.Character import Character
from app.models.Corporation import Corporation
from app.models.Division import Division
from masonite.facades import Auth
from app.esi.SSO import SSO
from masonite.request import Request
import requests

class CorporationController(Controller):
    """CorporationController Controller Class."""

    def index(self, view: View, request: Request):
        user = Auth.user()

        sso = SSO()
        character_id = request.input("character_id")

        if not character_id and user and user.characters.count() > 0:
            character_id = user.characters.first().character_id

        character = Character.where('character_id', character_id).first()
        corporation = character.corporation if character else None

        # get corp wallet info


        wallet = requests.get(f"https://esi.evetech.net/latest/corporations/{corporation.corporation_id}/wallets/", headers={
            "Authorization": f"Bearer {sso.get_access_token(request.cookie('eve_access_token'), request.cookie('eve_refresh_token'))}",
            "Content-Type": "application/json"
        })
        divisions = requests.get(f"https://esi.evetech.net/latest/corporations/{corporation.corporation_id}/divisions/", headers={
            "Authorization": f"Bearer {sso.get_access_token(request.cookie('eve_access_token'), request.cookie('eve_refresh_token'))}",
            "Content-Type": "application/json"
        })

        for division in divisions.json()['hangar']:
            print('division', division)
            # return division
            Division.update_or_create({
                'corporation_id': corporation.id,
                'division_id': division.get('division'),
            }, {
                'name': division.get('name', ''),
                'amount': 0,
            })
        for division in wallet.json():
            Division.update_or_create({
                'corporation_id': corporation.id,
                'division_id': division.get('division'),
            }, {
                'amount': division.get('balance', 0),
            })
    
        master_balance = 0
        total_balance = 0


        print('wallet json', wallet.json())

        for wallet_entry in wallet.json():
            if wallet_entry.get('division') == 1:
                master_balance = wallet_entry.get('balance', 0)
            
            total_balance += wallet_entry.get('balance', 0)

        
        divisions = Division.where('corporation_id', corporation.id).get()

        return view.render("eve.corphome", {
            "character": character,
            "characters": user.characters if user else [],
            'total_balance': total_balance,
            'master_balance': master_balance,
            'divisions': divisions,
            "corporation": corporation,
        })