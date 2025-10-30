from masonite.controllers import Controller
from masonite.request import Request
from masonite.response import Response
from app.models.Character import Character
from app.models.Corporation import Corporation
import requests
from masonite.configuration import config
import base64
from app.esi.SSO import SSO
from app.models.User import User
from masonite.auth import Sign
import pendulum

class CallbackController(Controller):


    def fetch(self, request: Request, response: Response):
        # Logic to handle the callback from EVE Online's SSO
        sso = SSO()
        base_64_encoded = sso.authorization_header_code()

        state = Sign().unsign(request.input("state"))
        user = User.find(state)  # Verify state matches a valid user session
        if not user:
            raise Exception("Unable to link character using state parameter "+state)


        # return "Basic " + base_64_encoded
        tokens = SSO().exchange_code_for_token(request.input("code"))

        response.cookie("eve_access_token", tokens.get("access_token", None), samesite="Lax")
        response.cookie("eve_access_token_expires", pendulum.now().add(seconds=tokens.get("expires_in", None)), samesite="Lax")
        response.cookie("eve_refresh_token", tokens.get("refresh_token", None), samesite="Lax")

        # get character info and add it to the characters table.
        character = requests.get("https://login.eveonline.com/oauth/verify", headers={
            "Authorization": f"Bearer {tokens.get('access_token')}"
        })
    
    
        info = requests.get(f"https://esi.evetech.net/characters/{character.json()['CharacterID']}/", headers={
            "Authorization": f"Bearer {tokens.get('access_token', None)}"
        })

        # print('character ', character.json())
        # print('character info', info.json())

        Character.update_or_create({
            'character_id': character.json()['CharacterID'],
        }, {
            'user_id': user.id,
            'name': info.json().get('name', ''),
            'description': info.json().get('description', ''),
            'birthday': info.json().get('birthday', None),
            'corporation_id': info.json().get('corporation_id', ''),
            'bloodline_id': info.json().get('bloodline_id', ''),
            'race_id': info.json().get('race_id', ''),
        })

        # get corp info and add it to the corporations table.

        corp = requests.get(f"https://esi.evetech.net/corporations/{info.json().get('corporation_id')}/", headers={
            "Authorization": f"Bearer {sso.get_access_token(tokens.get('access_token', None), tokens.get('refresh_token', None))}",
            "Content-Type": "application/x-www-form-urlencoded",
        })


        corporation = Corporation.first_or_create({
            'corporation_id': info.json().get('corporation_id'),
        }, {
            'name': corp.json().get('name', ''),
            'corporation_id': corp.json().get('corporation_id'),
            'ticker': corp.json().get('ticker', ''),
            'description': corp.json().get('description', ''),
            'alliance_id': corp.json().get('alliance_id', None),
            'date_founded': corp.json().get('date_founded', None),
            'member_count': corp.json().get('member_count', 0),
        }).fresh()


        corporation.update({
            'member_count': corp.json().get('member_count', 0),
            'ceo_id': corp.json().get('ceo_id', None),
        })


        Character.update_or_create({
            'character_id': character.json()['CharacterID'],
        }, {
            'user_id': user.id,
            'name': info.json().get('name', ''),
            'description': info.json().get('description', ''),
            "access_token": tokens.get("access_token", None),
            "refresh_token": tokens.get("refresh_token", None),
            'birthday': info.json().get('birthday', None),
            'corporation_id': corporation.id if corporation else None,
            'bloodline_id': info.json().get('bloodline_id', ''),
            'race_id': info.json().get('race_id', ''),
        })



        # return "check"
        return response.redirect("/dashboard/eve-home")