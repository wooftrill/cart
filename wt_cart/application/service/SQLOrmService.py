import os
import logging
from wt_cart.application.service.SQLClient import SQLClient
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from wt_cart.config.config import TABLE


class SQLOrmService(SQLClient):
    def __init__(self):
        super().__init__()
        self.__cart_table=TABLE["cart"]
        self.__inventory_table= TABLE["inventory"]

    def add_to_cart(self, data_model: dict, inventory_model: dict):
        logging.info("add_to_cart method called")
        try:
            count = self.count(self.__cart_table, data_model)
            if count >= 0:
                logging.info("item is already present in cart!! updating..")
                count = count+1
                if self.is_exist_in_inventory(self.__inventory_table,inventory_model):
                    if self.update_if_exist(self.__cart_table, data_model, count):
                        return True
        except Exception as ex:
            logging.info("item not present in cart ")
            if "Key Error" in str(ex):
                if self.is_exist_in_inventory(self.__inventory_table, inventory_model):
                    if self.insert(self.__cart_table, data_model):
                        return True

    def update_to_cart(self, data_model: dict, inventory_model: dict):
        logging.info("update function triggered!...")
        if self.is_exist_in_inventory(self.__inventory_table, inventory_model):
            if self.update(self.__cart_table, data_model):
                return True
            raise SQLAlchemyError("Could not update the cart.")
        raise IntegrityError("Item not present in directory!..")

    def remove_from_cart(self, data_model: dict):
        logging.info("remove function triggered!...")
        if self.update(self.__cart_table, data_model):
            return True
        raise SQLAlchemyError("Could not update the cart.")

    def show_cart_with_session(self, data_model:dict):
        logging.info("show cart  function triggered!...")
        return self.show_tbl(self.__cart_table, data_model)


sql_service = SQLOrmService()







#cart_table="cart"
#inventory_table="inventory"
#cart_model={"session_id":"wewewerdd","item_id":"c121","is_active":1,"count":4}
#inventory_model={"item_id":"c121"}
#cart_update_model={"session_id":"sess127","item_id":"c1219","is_active":1}

#print(SQLOrmService().show_cart_with_session(cart_model))











