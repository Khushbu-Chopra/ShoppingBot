from wit import Wit 

wit_access_token = "54DKTHZAZ5XKZYHYJS7WZFGWEJPZHJDW"
client = Wit(access_token = wit_access_token)

def wit_response(message_text):
	resp = client.message(message_text)
	categories = {'Shopping':None, 'category':None,'Start':None}

	
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	
	return categories
