import os
import logging
import time,requests
import requests,time
from flask import request
from functools import wraps
from wt_cart.config.config import TABLE
from wt_cart.application.service.SQLClient import sql_client


class AddressVerification:
    def __init__(self):
        self.__pin_table = TABLE["pin"]
        self.__address_table = TABLE["user_address"]
        pass

    def get_address_verified(self,func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            adress_code = request.json["address_code"]
            cost_obj= sql_client.show_pin(self.__address_table,self.__pin_table,adress_code)
            checkout_obj = func(cost_obj,*args, ** kwargs)
            return checkout_obj
        return decorated_function








address_verification=AddressVerification()
