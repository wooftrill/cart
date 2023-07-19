import os
import logging
from wt_cart.application.service.SQLClient import SQLClient
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from wt_cart.application.model.InventoryModel import InventoryModel
from dataclasses import asdict
from wt_cart.config.config import TABLE


class SQLOrmService(SQLClient):
    def __init__(self):
        super().__init__()
        self.__cart_table=TABLE["cart"]
        self.__link_table=TABLE["link"]
        self.__inventory_table= TABLE["inventory"]

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
        cart = self.show_tbl_with_login(self.__cart_table, data_model, self.__link_table, uid)
        if len(cart) == 0:
            return False
        else:
            available_list=[]
            non_available_list=[]
            net_cost=0
            final_output= {}
            logging.info("found cart items")
            for item in cart:
                inventory_model = asdict(InventoryModel(item["item_id"]))
                inventory_status = self.is_exist_in_inventory(self.__inventory_table, inventory_model)
                if inventory_status[2] > item["count"]:
                    available_list.append(item)
                else:
                    non_available_list.append(item)
            for element in available_list:
                net_cost = net_cost+element["net_cost"]
            final_output["available"] = available_list
            final_output["net_total"] = net_cost
            final_output["unavailable"] = non_available_list
            return final_output


sql_service = SQLOrmService()







#cart_table="cart"
#inventory_table="inventory"
#cart_model={"session_id":"wewewerdd","item_id":"c121","is_active":1,"count":4}
#inventory_model={"item_id":"c121"}
#cart_update_model={"session_id":"sess127","item_id":"c1219","is_active":1}
datamodel={"session_id":"debtest56mou78012testl","cart_id":"debtest56mou78012testl","item_id":"","count":1,"is_active":1}
print(SQLOrmService().check_out_with_login(datamodel,"u5AP2SioTfQaAWeKake8zOl2fdd2"))











