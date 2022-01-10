import requests
import time
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

def send_SMS(text, toNumber):
	# Singup on twilio and you get a free number to send SMSes
	# Paste in your accountSid,authToken and fromNumber from your twilio profile
	accountSid = "AXXXX"
	authToken ="XXX"
	fromNumber = +1123456789
  
	client = Client(accountSid, authToken)
	message = client.messages \
	                .create(
	                     body=text,
	                     from_=fromNumber,
	                     to=toNumber
	                 )



# Website to check
url = 'https://summitatsnoqualmie.com'
# Update with the initial message on the website
text_to_check = "Due to the extended closure of I-90 over Snoqualmie Pass, all Summit areas will be temporarily closed today, Thursday, Jan 6. All lift tickets for today will be automatically extended and can be used on another date this season. Operations for Friday, Jan 7 are currently TBD and dependent on the opening of I-90. We'll continue to provide updates as we have them."

# Your own cell number
toNumber = +1

while True:
	try:
	
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")

		# You can scrap anyother site by just changing the value of url above
		# and modify the below line to extract the info you are looking for from the html class
		general_data = soup.find_all('div', {'class' : 'quarantine text text_16 mix-text_color1 box_bottom2'})

		text_fetched = general_data[0].contents[1].text
		if text_to_check != text_fetched:
			# Update the exact value for you want to send
			send_SMS("Message on summitatsnoqualmie.com changed. \nLatest message = " + text_fetched, toNumber)

			# Update the value of text_to_check so that from this point on you are 
			# notified only if the message on the website changes
			text_to_check = text_fetched
			print("SMS sent")
		else:
			print("No diff found")
		
		# Wait for 1hr before hitting the website again
		time.sleep(3600)

	except Exception as e:
		send_SMS("Script failed "+ e.messages, toNumber)


