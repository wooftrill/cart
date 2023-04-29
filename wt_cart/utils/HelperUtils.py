import os
import logging


class HelperUtils:

    @staticmethod
    def tupple_to_dict(sql_response_list: list):
        keys = ["session_id", "item_id", "count","is_active"]
        json_list = []
        for tpl in sql_response_list:
            json_dict = {}
            for i in range(len(tpl)):
                json_dict[keys[i]] = tpl[i]
            json_list.append(json_dict)
        return json_list



