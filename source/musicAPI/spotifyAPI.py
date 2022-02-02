import base64
import requests
import datetime
from urllib.parse import urlencode
from rest_framework import status

class SpotifyAPI(object):
    access_token = None
    token_expires = datetime.datetime.now()
    token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_credentials(self):
        if self.client_secret == None or self.client_id == None:
            raise Exception('You must set client_id and client_secret')
        
        return base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()

    def get_token_headers(self):
        return {
            'Authorization': f'Basic {self.get_credentials()}'
        }

    def get_token_data(self):
        return {
            'grant_type': 'client_credentials'
        }
    
    def get_access_token(self):
        if datetime.datetime.now() > self.token_expires:
            self.auth()
        return self.access_token

    def auth(self):
        r = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_headers())
        if r.status_code not in range(200, 299):
            raise Exception('Could not authenticate client.')
        
        data = r.json()
        self.access_token = data['access_token']
        now = datetime.datetime.now()
        self.token_expires = now + datetime.timedelta(seconds=data['expires_in'])
        self.token_did_expire = self.token_expires < now
        return True
    
    def get_resource_header(self):
        return 

    def q_dict(self, q):
        return ' '.join([f'{k}:{v}' for k, v in q.items()])

    def search(self, q, operator, operator_q, search_type='track'):
        if isinstance(q, dict):
            q = self.q_dict(q)
        if operator != None and operator_q != None:
            operator = operator.upper()
            if operator == 'OR' or operator == 'NOT':
                if isinstance(operator_q, dict):
                    operator_q = self.q_dict(operator_q)
                q = f'{q} {operator} {operator_q}'

        query = urlencode({'q': q, 'type': search_type.lower()})

        r = requests.get(f'https://api.spotify.com/v1/search?{query}', headers={
            'Authorization': f'Bearer {self.access_token}'
        })
        if r.status_code in range(200, 299):
            return r.json()
        return dict()

    def get_resource(self, id, resource_type, version='v1'):
        r = requests.get(f'https://api.spotify.com/{version}/{resource_type.lower()}/{id}', headers={
            'Authorization': f'Bearer {self.access_token}'
        })
        
        if r.status_code in range(200, 299):
            return r.json()
        return dict()
    
    def get_artist(self, id):
        '''
        Gets an Artist object when given an id
        '''
        return self.get_resource(id, resource_type='artist')

    def get_track(self, id):
        '''
        Gets a Track object when given an id
        '''
        return self.get_resource(id, resource_type='track')

    def get_album(self, id):
        '''
        Gets an Album object when given an id
        '''
        return self.get_resource(id, resource_type='album')