from datetime import date, datetime, timedelta
import requests
import json


def sendAlertToSlack(webh):
     today = datetime.now().strftime('%Y-%m-%d')

     # Here is where we can format the slack message, it will output any holiday with todays
     message = f'Balloon Detected - ' + today
     print('Sending message to the balloons-detection-system channel...')
     slackmsg = {'text': message}

     # Using the module json it formats it where the slack API can accept it
     # we can store the slack link into a variable called webhook
     webhook = webh
     response = requests.post(webhook, data=json.dumps(slackmsg), headers={'Content-Type': 'application/json'})

     if response.status_code != 200:
          raise ValueError(
               'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))
     else:
          print('Request completed!')


