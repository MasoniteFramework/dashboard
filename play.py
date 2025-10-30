from app.esi.ESIClient import ESIClient


client = ESIClient()

print(client.set_tokens().verify_token())
