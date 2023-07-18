import  os
import logging

logging.getLogger().setLevel(logging.INFO)


class SQLUtils:
    """
    class for generating query
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def insert_query(table_name: str,args):
        return f"INSERT INTO external.{table_name} VALUES {args};"

    @staticmethod
    def exist_query(table_name: str, session: str, item_id: str):
        return f" SELECT count from {table_name} where session_id='{session}' and item_id='{item_id}'"

    @staticmethod
    def is_product_exist(table_name: str,item_id: str):
        return f"SELECT count,mrp from {table_name} where items_id='{item_id}';"

    @staticmethod
    def update_product(table_name: str, count: int, item_id: str, session: str, is_active: str, cost: float):
        return f"Update external.{table_name} SET count={count}, is_active={is_active}, net_cost={count}*{cost} where item_id='{item_id}'and session_id='{session}';"

    @staticmethod
    def simple_update_status(table_name: str, item_id: str, session: str):
        return f"Update external.{table_name} SET count= 0, is_active= 0 where item_id='{item_id}'and session_id='{session}';"

    @staticmethod
    def show_cart_wo_login(table_name: str, session: str):
        return f"select * from external.{table_name} where session_id='{session}' and is_active= true;"

    @staticmethod
    def show_cart_with_login(table_name : str, link_table: str, uid:str,session_id: str):
        return f"SELECT DISTINCT {table_name}.session_id, {table_name}.item_id, {table_name}.count, {table_name}.cost,{table_name}.net_cost,{table_name}.cart_id FROM external.{table_name}  INNER JOIN external.{link_table}  ON {table_name}.session_id = {link_table}.cart  WHERE {link_table}.uid = '{uid}' AND curr_session = '{session_id}' AND {link_table}.is_sold = false  AND {table_name}.is_active = 1;"



print(SQLUtils.show_cart_with_login('tbl_cart', 'tbl_user_session_cart','c88b46f5be0eee347e50a72b0daa371b4cc8a857','debtest56mou78012testl'))