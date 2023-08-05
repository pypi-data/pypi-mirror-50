from time import sleep
from json import loads
from requests import get


class InfinityCoinPoll(object):
    def __init__(self, infinity_coin_object):
        self.infinity_coin_object = infinity_coin_object
        self.last_transfer = self.infinity_coin_object.history()[0]['id']
    
    def listen(self, timeout=3):
        while True:
            history = self.infinity_coin_object.history()
        
            for payment in history:
                if payment['id'] > self.last_transfer:
                    yield payment
                else:
                    break
                
            self.last_transfer = history[0]['id']
            
            sleep(timeout)