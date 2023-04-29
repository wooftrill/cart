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
        return f"SELECT count from {table_name} where item_id='{item_id}';"

    @staticmethod
    def update_product(table_name: str, count: int, item_id: str, session: str, is_active: str):
        return f"Update external.{table_name} SET count={count}, is_active={is_active} where item_id='{item_id}'and session_id='{session}';"

    @staticmethod
    def show_cart_wo_login(table_name: str, session: str):
        return f"select * from external.{table_name} where session_id='{session}' and is_active='1';"



