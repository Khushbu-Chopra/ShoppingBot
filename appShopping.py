import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAGuNe0EhHcBAEryY8PUnUjfkczRh83aLjyDF9Uw31k33byAfKZCe8p7W6IZAQd3Xg5KbHUiZBqGiKojfz0G2XZAwUFAdOpTlZBD8cA1IT2wnxVbroTFrRmD5E9MvNYiDNr8C6zIZCr5FyU9iUij9n3kmg0bejB5Fe6RPLFZCGLugZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)
shopMen = {'Accessories':['Belt','Cufflink','Pocket Square','Tie','Wallet'],
		   'Indian Wear':['Kurta','Nehru Jacket','Sherwani'],
		   'Bottomwear':['Pant','Shorts','Tracks','Trousers'],
		   'Footwear':['Flip flops','Floaters','Shoes','Slippers','Sneakers'],
		   'Topwear':['Blazer','Coat','Jacket','Shirt','Suit','Sweater','Sweatshirt']}
shopWomen = {'Western Wear':['Blazer','Capri','Coat','Dress','Jacket','Jeans','Jegging','Jumpsuit','Shirt','Shorts','Shrug','Skirt','Sweater','Sweatshirt','T-Shirt','Trouser','Waistcoat'],
			 'Footwear':['Flats','Floaters','Shoes','Heels'],
			 'Jewellery':['Fine jewellery','Boutique Jewellery','Fashion jewellery'],
			 'Indian and Fushion Wear':['Blouse','Churidar','Dupatta','Kurti','Legging','Palazzo','Salwar','Saree','Shawl','Skirt','Top','Tunic'],
			 'Handbags, Wallets and Bags':['Bag','Handbag','Purse','Sling bag','Wallet']}
shopKids = {'Boys Clothing':['Indian Wear','Jeans','Pyjama','Shirt','Shorts','Sweater','Sweatshirt','T-Shirt','Tracks','Trouser'],
			'Girls Clothing':['Capri','Dress','Jeans','Jumpsuit','Legging','Shorts','Skirt','Sweater','Sweatshirt','T-Shirt','Tracks','Trouser','Tights','Top'],
			'Boys Footwear':['Flip flop','Sandals','Shoes'],
			'Girls Footwear':['Flip flop','Sandals','Shoes','Heels','Flats'],
			'Kids Accessories':['Backpack','Bag','Hair accessory','Sunglasses','Watch']}
responseMen = ''
responseWomen = ''
responseKids = ''
for key in shopMen.keys() :
   	responseMen = responseMen + str(key) + '\n'
for key in shopWomen.keys() :
   	responseWomen = responseWomen + str(key) + '\n'
for key in shopKids.keys() :
   	responseKids = responseKids + str(key) + '\n'
#print(responseMen+'\n'+responseWomen+'\n'+responseKids)
@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'

					response = None #format(str(value))

					categories = wit_response(messaging_text)
					if categories['Start']!=None:
						response0="Hello. Welcome to Shopping Bot!"
						bot.send_text_message(sender_id,response0)
					if categories['category']==None:
						response = "What would you like to shop for: \nMen \nWomen \nKids \nKindly enter the category."
						bot.send_text_message(sender_id,response)
					elif categories['category']=='Men':
						response = "You've chosen 'Men' as the category. What are you looking for?"
						bot.send_text_message(sender_id,response)
						bot.send_text_message(sender_id,responseMen)
					elif categories['category']=='Women':
						response = "You've chosen 'Women' as the category. What are you looking for?"
						bot.send_text_message(sender_id,response)
						bot.send_text_message(sender_id,responseWomen)
					elif categories['category']=='Kids':
						response = "You've chosen 'Kids' as the category. What are you looking for?"
						bot.send_text_message(sender_id,response)
						bot.send_text_message(sender_id,responseKids)
	return "ok", 200


def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)