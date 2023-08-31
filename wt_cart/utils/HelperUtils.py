import os
import logging
import hashlib,json
import time,uuid


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
    def get_timestamp():
        time_stamp = int(time.time_ns())
        return time_stamp

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

    @staticmethod
    def create_uuid():
        curr_time= time.time_ns()
        print(curr_time)
        sufix= uuid.uuid4().int & ((1 << 16) - 1)
        uuid_from_timestamp = uuid.UUID(int=curr_time*2 + sufix)
        return str(uuid_from_timestamp)

    @staticmethod
    def create_combine_list(list_name):
        count_dict = {}

        for data in list_name:
            item = data["item_id"]
            count = data["count"]
            count_dict[item] = count_dict.get(item, 0) + count

        result_list = [{"item_id": item, "count": count} for item, count in count_dict.items()]

        return result_list

    @staticmethod
    def find_wt_discount(net_cost,discount_list):
        for element in discount_list:
            if element["valid_from"] < net_cost < element["valid_upto"]:
                return element["discount_id"],element["total_discount_in_prcnt"]

    @staticmethod
    def find_vendor_discount(discount_id,discount_list):
        for element in discount_list:
            if element["discount_id"] == discount_id:
                return element["total_discount_in_prcnt"]
        return False







