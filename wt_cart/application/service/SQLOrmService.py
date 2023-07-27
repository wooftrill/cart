import json
import os
import logging
from wt_cart.application.service.SQLClient import SQLClient
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from wt_cart.utils.HelperUtils import HelperUtils
from wt_cart.application.model.InventoryModel import InventoryModel
from dataclasses import asdict
from wt_cart.config.config import TABLE


class SQLOrmService(SQLClient):
    def __init__(self):
        super().__init__()
        self.__cart_table=TABLE["cart"]
        self.__link_table=TABLE["link"]
        self.__inventory_table= TABLE["inventory"]
        self.__checkout_table=TABLE["checkout"]

    def add_to_cart(self, data_model: dict, inventory_model: dict):
        logging.info("add_to_cart method called")
        try:
            count = self.count(self.__cart_table, data_model)
            if count >= 0:
                logging.info("item is already present in cart!! updating..")
                count = count+1
                inventory_status = self.is_exist_in_inventory(self.__inventory_table,inventory_model)
                if inventory_status[0]:
                    if self.update_if_exist(self.__cart_table, data_model, count,inventory_status[1]):
                        return True
        except Exception as ex:
            logging.info("item not present in cart ")
            if "Key Error" in str(ex):
                inventory_status = self.is_exist_in_inventory(self.__inventory_table, inventory_model)
                if inventory_status[0]:
                    if self.insert(self.__cart_table, data_model, (inventory_status[1], inventory_status[1])):
                        return True

    def update_to_cart(self, data_model: dict, inventory_model: dict):
        logging.info("update function triggered!...")
        inventory_status = self.is_exist_in_inventory(self.__inventory_table, inventory_model)
        if inventory_status[0]:
            if self.update(self.__cart_table, data_model, inventory_status[1]):
                return True
            raise SQLAlchemyError("Could not update the cart.")
        raise IntegrityError("Item not present in directory!..")

    def remove_from_cart(self, data_model: dict):
        logging.info("remove function triggered!...")
        if self.simple_update(self.__cart_table, data_model):
            return True
        raise SQLAlchemyError("Could not update the cart.")

    def show_cart_with_session(self, data_model:dict):
        logging.info("show cart  function triggered!...")
        return self.show_tbl(self.__cart_table, data_model)

    def show_cart_with_login(self, data_model:dict,uid: str):
        logging.info("show cart  function triggered!...")
        return self.show_tbl_with_login(self.__cart_table, data_model,self.__link_table, uid)

    def check_out_with_login(self, data_model: dict, uid: str):
        logging.info("checkout function triggered!...")
        cart_total = self.show_tbl_with_login(self.__cart_table, data_model, self.__link_table, uid)

        cart = HelperUtils.create_combine_list(cart_total)
        print(cart)
        if len(cart) == 0:
            return False
        else:
            dict_av={}
            available_list=[]
            non_available_list=[]
            net_cost_av,net_cost_nav= 0, 0
            final_output= {}
            logging.info("found cart items")
            order_id = HelperUtils.create_uuid()
            for item in cart:
                inventory_model = asdict(InventoryModel(item["item_id"]))
                inventory_status = self.is_exist_in_inventory(self.__inventory_table, inventory_model)
                available_item= inventory_status[2] - TABLE["HardLimit"]

                if available_item > item["count"]:
                    item["cost"]= inventory_status[1]
                    item["net_cost"] = int(item["cost"])*item["count"]
                    available_list.append(item)

                else:
                    if available_item > 0:
                        dict_av["item_id"] = item["item_id"]
                        dict_av["count"] = available_item
                        dict_av["cost"] = int(inventory_status[1])
                        dict_av["net_cost"] = dict_av["cost"] * dict_av["count"]
                        available_list.append(dict_av)
                    item["count"] = item["count"] - available_item
                    item["cost"] = int(inventory_status[1])
                    item["net_cost"] = item["cost"] * item["count"]
                    non_available_list.append(item)
            if len(available_list)>0:
                final_output["available_order_no"]= order_id+"-00"

            if len(non_available_list)>0:
                final_output["non_available_order_no"]= order_id+"-01"

            for element in available_list:
                net_cost_av = net_cost_av+element["net_cost"]
            for element in non_available_list:
                net_cost_nav = net_cost_nav + element["net_cost"]

            final_output["order_id"] = order_id
            final_output["available"] = available_list
            final_output["net_total"] = net_cost_av+ net_cost_nav
            final_output["unavailable"] = non_available_list
            final_output["session_id"] = data_model["session_id"]

            check_model={"uid": uid,"session_id": data_model["session_id"],"checkout_value": json.dumps(final_output)}
            print(self.checkout_count(self.__checkout_table, check_model))
            if self.checkout_count(self.__checkout_table,check_model)> 0:
                logging.info("checkout table updated..")
                if self.update_checkout(self.__checkout_table,check_model):
                    return final_output
            else:

                logging.info("no record found with same uid & sessionid . Inserting...")
                if self.insert(self.__checkout_table,check_model,()):
                    return final_output


sql_service = SQLOrmService()







#cart_table="cart"
#inventory_table="inventory"
#cart_model={"session_id":"wewewerdd","item_id":"c121","is_active":1,"count":4}
#inventory_model={"item_id":"c121"}
#cart_update_model={"session_id":"sess127","item_id":"c1219","is_active":1}
datamodel={"session_id":"debtes899997jkjghg-jhhjghvbv86","cart_id":"debtes899997jkjghg-jhhjghvbv86","item_id":"","count":1,"is_active":1}

print(SQLOrmService().check_out_with_login(datamodel,"u5AP2SioTfQaAWeKake8zOl2fdd2"))











