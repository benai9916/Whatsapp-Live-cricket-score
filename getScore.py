
import requests
from datetime import datetime as dt

class getScore:
    def __init__(self):
        # match end point
        self.get_all_matchs = 'https://cricapi.com/api/matches/'
        # End point to get the live score
        self.get_match_score = 'https://cricapi.com/api/cricketScore/'
        self.API_Key = 'CRIC-API-TOKEN'
        self.unique_id = []

    def get_unique_id(self):
        # setting the parameter to request
        uri_params = {'apikey': self.API_Key}
        resp = requests.get(self.get_all_matchs, params=uri_params)
        match_resp = resp.json()
        uid_found = 0

        for  match in match_resp['matches']:
            # Enable the below line if you want the update only for specific country and ypu can enter country name
            # also uncomment the break in this case
            # if(match['team-1'] == 'India' or match['team-2'] == 'India' and match['matchStarted'] == True):
            if (match['matchStarted'] == True):
                # Enable the below code code if you want today match
                # todays_date = dt.today().strftime('%y-%m-%d')
                # if todays_date == match['date'].split('T')[0]:
                self.unique_id.append(match['unique_id'])
                uid_found = 1
                # break
 
        if not uid_found:
            self.unique_id = -1

        for id_list in self.unique_id[1:]:
            send_score = self.get_current_score(id_list)
            return send_score

    def get_current_score(self, unique_id):
        data = ''
        if unique_id == -1:
            data = 'no matched today'
        else:
            uri_params = {'apikey': self.API_Key,'unique_id': unique_id}
            resp = requests.get(self.get_match_score,params = uri_params)
            score_data =  resp.json()

            try:
                # get the comment and score of the match
                data =  'here is the score: \n' + score_data['stat']+'\n'+score_data['score']
            except KeyError as e:
                print(e)

        return data

if __name__ == "__main__":
    object_score = getScore()
    list_of_all_score = object_score.get_unique_id()

    # Sign in to twilio and get ACCOUNT-SID TOKEN and AUTH TOKEN
    from twilio.rest import Client
    a_sid = 'ACCOUNT-SID TOKEN'
    auth_toke = 'AUTH TOKEN'

    client = Client(a_sid, auth_toke)
    # please add ypur number to receive a message
    message = client.messages.create(body=list_of_all_score, from_='whatsapp:+14155238886',to='whatsapp:+91YOUR-WHATSAPP-NUMBER')
