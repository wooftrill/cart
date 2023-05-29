import os
import logging
import hashlib,json


class HelperUtils:

    @staticmethod
    def generate_hash(obj: str):
        """
        :param email:
        :return:
        """
        if obj:
            return hashlib.sha1(obj.encode()).hexdigest()

    @staticmethod
    def tupple_to_dict(sql_response_list: list,keys: list):
        #keys = ["session_id","cart_id", "item_id", "count","is_active"]
        json_list = []
        print(sql_response_list)
        for tpl in sql_response_list:
            json_dict = {}
            for i in range(len(tpl)):
                json_dict[keys[i]] = tpl[i]
            json_list.append(json_dict)
        return json_list



