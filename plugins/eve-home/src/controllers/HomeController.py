from masonite.controllers import Controller
from masonite.views import View
from app.models.User import User
from app.models.Character import Character
from app.models.IndustryJob import IndustryJob
from app.models.WalletTransactions import WalletTransaction
from app.models.Item import Item
from masonite.configuration import config
from masonite.request import Request
from masonite.auth import Sign
import requests
from masonite.facades import Auth
from app.esi.SSO import SSO
import pendulum
import math

class HomeController(Controller):
    def index(self, view: View, request: Request):
        character_id = 291969501
        sso = SSO()

        user = Auth.user()
        
        # Fetch character data
        base_64_encoded = sso.authorization_header_code()


        print('user', user)



        

        character_id = request.input("character_id")

        if not character_id and user and user.characters.count() > 0:
            character_id = user.characters.first().character_id
        
        # print('character_id', character_id)

        character = Character.where('character_id', character_id).first()


        corporation = character.corporation if character else None


        # eve jobs test

        jobs = requests.get(f"https://esi.evetech.net/latest/characters/{character_id}/industry/jobs/", headers={
            "Authorization": f"Bearer {sso.get_access_token(request.cookie('eve_access_token'), request.cookie('eve_refresh_token'))}",
            "Content-Type": "application/json"
        })

        print('jobs', jobs.content)
        
        

        
        
        return view.render("eve.home", {
            "character": character,
            "characters":user.characters,
            "corporation": corporation,
            "sign": Sign(),
            'portrait_url': f"https://images.evetech.net/characters/{character.character_id}/portrait?size=256"
        })

    def industry_jobs(self, view: View, request: Request):
        user = Auth.user()

        sso = SSO()
        character_id = request.input("character_id")

        if not character_id and user and user.characters.count() > 0:
            character_id = user.characters.first().character_id

        character = Character.where('character_id', character_id).first()


        if request.input("refresh") == "1":
            jobs = requests.get(f"https://esi.evetech.net/latest/characters/{character_id}/industry/jobs/", headers={
                "Authorization": f"Bearer {sso.get_access_token(character.access_token, character.refresh_token)}",
                "Content-Type": "application/json"
            })
            for job in jobs.json():
                IndustryJob.update_or_create({
                    'job_id': job.get('job_id'),
                }, {
                    'character_id': character.id,
                    'status': job.get('status'),
                    'activity_id': job.get('activity_id'),
                    'blueprint_id': job.get('blueprint_id'),
                    'blueprint_type_id': job.get('blueprint_type_id'),
                    'cost': job.get('cost'),
                    'duration': job.get('duration'),
                    'start_date': job.get('start_date'),
                    'end_date': job.get('end_date'),
                    'licensed_runs': job.get('licensed_runs', None),
                    'probability': job.get('probability', None),
                    'runs': job.get('runs', None),
                })




                item = requests.get(f"https://esi.evetech.net/universe/types/{job['blueprint_type_id']}", headers={
                    "Authorization": f"Bearer {sso.get_access_token(character.access_token, character.refresh_token)}",
                    "Content-Type": "application/json"
                }).json()

                
                if Item.where("item_id", item['type_id']).count() == 0:
                    Item.first_or_create({
                        "item_id": item['type_id'],
                    }, {
                        "item_id": item['type_id'],
                        "name": item['name'],
                        "description": item['description'],
                        "volume": item['volume'],
                        "packaged_volume": item['packaged_volume'],
                        "graphic_id": item['graphic_id'],
                    })




        count = str(IndustryJob.where('character_id', character.id).where('status', 'active').count())

        return view.render("eve.industry", {
            "character": character,
            "characters":user.characters,
            "pendulum": pendulum,
            "active_jobs":count,
            "round":round,
            "jobs": IndustryJob.where('character_id', character.id).get(),
            "sign": Sign(),
            'portrait_url': f"https://images.evetech.net/characters/{character.character_id}/portrait?size=256"
        })

    def wallet(self, view: View, request: Request):
        user = Auth.user()

        sso = SSO()
        character_id = request.input("character_id")

        if not character_id and user and user.characters.count() > 0:
            character_id = user.characters.first().character_id

        character = Character.where('character_id', character_id).first()


        if request.input("refresh") == "1":
            wallet_transactions = requests.get(f"https://esi.evetech.net/latest/characters/{character_id}/wallet/journal/", headers={
                "Authorization": f"Bearer {sso.get_access_token(character.access_token, character.refresh_token)}",
                "Content-Type": "application/json"
            }).json()

            # 
    
            for transaction in wallet_transactions:
                    # print('transaction', transaction)
                    transaction_type = "Uncategorized"

                    if  transaction.get("amount", 0) > 0:
                        transaction_type = "Income"
                    elif transaction.get("amount", 0) < 0:
                        transaction_type = "Expense"


                    WalletTransaction.update_or_create({
                        'journal_id': transaction.get('id'),
                    }, {
                        "journal_id": transaction.get("id"),
                        "amount": transaction.get("amount"), 
                        "balance": transaction.get("balance"),
                        "reason": transaction.get("reason"),
                        "ref_type": transaction.get("ref_type"),
                        "character_id": character.id,
                        "quantity": None,
                        "transaction_id": transaction.get("id"),
                        "transaction_date": transaction.get("date"),
                        "transaction_type": transaction_type,
                    })


        transactions = WalletTransaction.where("character_id", character.id).order_by("transaction_date", "desc").get()

        current_balance = transactions.max("balance") if transactions.count() > 0 else 0

        total_income = sum([t.amount for t in transactions if t.transaction_type == "Income"])
        total_expenses = sum([t.amount for t in transactions if t.transaction_type == "Expense"])
        net_profit = total_income + total_expenses


        wallet = requests.get(f"https://esi.evetech.net/latest/characters/{character_id}/wallet/", headers={
            "Authorization": f"Bearer {sso.get_access_token(character.access_token, character.refresh_token)}",
            "Content-Type": "application/json"
        }).json()


        print('wallet', wallet)

        return view.render("eve.wallet", {
            "character": character,
            "characters":user.characters,
            "wallet_transactions": transactions,
            "pendulum": pendulum,
            "round": round,
            "current_balance": float(wallet),
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            # "sign": Sign(),
            # 'portrait_url': f"https://images.evetech.net/characters/{character.character_id}/portrait?size=256"
        })