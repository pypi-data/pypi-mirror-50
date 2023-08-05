from json import loads
from requests import get

from .exceptions import *


class InfinityCoin(object):
    API_URL = 'https://ic.studiofox.space/api/'
    APP_URL = 'https://vk.com/app6954459'
    
    def __init__(self, key):
        self.key = key
        self.__auth()
    
    def __request(self, params):
        try:
            data = {'key': self.key}
            data.update(params)
            response = get(self.API_URL, params=data)
            response = loads(response.text)
        except:
            raise InfinityCoinError('Error connecting to server')
        
        if 'response' in response.keys():
            code = int(response['response']['code'])
            if code == 200:
                return response['response']
            else:
                raise InfinityCoinError(f'Server returned an unknown code: {code} (response)')
        elif 'error' in response.keys():
            code = int(response['error']['code'])
            
            if code == 401:
                raise Unauthorized
            elif code == 405:
                raise MethodNotFound
            elif code == 422:
                raise InvalidGETParam
            else:
                raise InfinityCoinError(f'Server returned an unknown code: {code} (error)')
        else:
            raise InfinityCoinError(f'The server returned some crap.../n{response.text}')
    
    def __auth(self):
        self.score()
    
    @classmethod
    def get_fast_link(toid, amount=None):
        if amount is None:
            return f'{self.APP_URL}#t{toid}'
        else:
            return f'{self.APP_URL}#t{toid}_{amount}'
    
    def history(self):
        return self.__request({'method': 'history'})['data']
    
    def score(self):
        return self.__request({'method': 'score'})['data']
    
    def transfer(self, toid, amount):
        return self.__request({'method': 'transfer', 'toid':toid, 'amount':amount})['msg']