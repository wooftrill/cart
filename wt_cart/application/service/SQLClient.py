import os
import logging
import time

from wt_cart.utils.SQLUtils import SQLUtils
from wt_cart.utils.HelperUtils import HelperUtils
from wt_cart.config.config import MYSQL
from sqlalchemy.sql import text
from sqlalchemy.exc import *
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer,Table,String,MetaData


class SQLClient:

    def __init__(self) ->None:
        self.sql_conn = f"mysql+pymysql://{MYSQL['user']}:mypassword@localhost:3306/external"
        self.engine = create_engine(self.sql_conn)

        pass

    def insert(self, table_name: str, sql_model: dict):
        try:
            logging.info("checking if table exist!!...")
            inspect_db = sa.inspect(self.engine)
            is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
            if not is_exist:
                raise NoSuchTableError
            else:
                curr_session = sessionmaker(bind=self.engine)
                session = curr_session()
                query = SQLUtils.insert_query(table_name, tuple(sql_model.values()))
                response = session.execute(text(query))
                if response.__dict__['rowcount'] > 0:
                    logging.info("row inserted!..")
                    return True
                raise SQLAlchemyError("Error!...no row affected")
        except DataError as e:
            session.rollback()
            logging.error(f"Insert failed: {e}")
        except Exception as ex:
            session.rollback()
            logging.error(f"issue with query:{ex}")
        finally:
            session.commit()
            session.close()
            logging.info("session closed")

    def is_exist_in_inventory(self, table_name: str, inventory_model: dict):
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    query = SQLUtils.is_product_exist(table_name, inventory_model["item_id"])
                    count_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        count_list.append(res[0])
                    if count_list[0] > __min_available:
                        return True
                    return False
            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

        raise Exception("Could not perform database eration after {} retries".format(max_retries))

    def count(self, table_name: str, sql_model: dict):
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    query = SQLUtils.exist_query(table_name, sql_model["session_id"],sql_model["item_id"])
                    count_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        count_list.append(res[0])
                    print(count_list)
                    return count_list[0]

            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except IntegrityError as ix:
                logging.error("key error {}".format(ix))
                raise ix
            except IndexError as ix:
                logging.error("key error {}".format(ix))
                raise Exception( f"Key Error: {ix}")

            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

        raise Exception("Network error :Could not perform database eration after {} retries".format(max_retries))

    def update(self,table_name, sql_model):
        """

        :param table_name:
        :param sql_model:
        :return:
        :purpose: updating from cart section
        """
        try:
            logging.info("checking if table exist!!...")
            inspect_db = sa.inspect(self.engine)
            is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
            if not is_exist:
                raise NoSuchTableError
            else:
                curr_session = sessionmaker(bind=self.engine)
                session = curr_session()
                query = SQLUtils.update_product(table_name,count=sql_model["count"],is_active=sql_model["is_active"],
                                                item_id=sql_model["item_id"], session= sql_model["session_id"])
                print(query)
                response = session.execute(text(query))
                if response.__dict__['rowcount'] > 0:
                    logging.info("row inserted!..")
                    return True
                raise SQLAlchemyError("Error!...no row affected")

        except OperationalError as e:
            logging.error("Error: connection issue {}".format(e))

        except DataError as e:
            session.rollback()
            logging.error(f"Insert failed: {e}")
        except Exception as ex:
            session.rollback()
            logging.error(f"issue with query:{ex}")
        finally:
            session.commit()
            session.close()
            logging.info("session closed")

    def update_if_exist(self, table_name: str, sql_cart_model:dict,count:int):
        """

        :param sql_cart_model:
        :param count:
        :param table_name:

        :return:
        :purpose: updating from cart section
        """
        try:
            logging.info("checking if table exist!!...")
            inspect_db = sa.inspect(self.engine)
            is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
            if not is_exist:
                raise NoSuchTableError
            else:
                curr_session = sessionmaker(bind=self.engine)
                session = curr_session()
                query = SQLUtils.update_product(table_name, count=count, is_active=sql_cart_model["is_active"],
                                                item_id=sql_cart_model["item_id"], session=sql_cart_model["session_id"])

                response = session.execute(text(query))
                if response.__dict__['rowcount'] > 0:
                    logging.info("row inserted!..")
                    return True
                raise SQLAlchemyError("Error!...no row affected")

        except OperationalError as e:
            logging.error("Error: connection issue {}".format(e))

        except DataError as e:
            session.rollback()
            logging.error(f"Insert failed: {e}")
        except Exception as ex:
            session.rollback()
            logging.error(f"issue with query:{ex}")
        finally:
            session.commit()
            session.close()
            logging.info("session closed")

    def show_tbl_with_login(self, table_name: str, sql_model: dict,link_table: str, uid: str):
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    uid= HelperUtils.generate_hash(uid)
                    query = SQLUtils.show_cart_with_login(table_name,link_table,uid, sql_model["session_id"])
                    print(query)
                    cart_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        cart_list.append(res)
                    return HelperUtils.tupple_to_dict(cart_list,["session_id","item_id","count"])
            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

        raise Exception("Could not perform database eration after {} retries".format(max_retries))

    def show_tbl(self, table_name: str, sql_model: dict):
        __min_available = 1
        max_retries = 3
        retries = 0
        logging.info("checking if table exist!!...")
        while retries < max_retries:
            try:
                inspect_db = sa.inspect(self.engine)
                is_exist = inspect_db.dialect.has_table(self.engine.connect(), table_name, schema="external")
                if not is_exist:
                    raise NoSuchTableError
                else:
                    curr_session = sessionmaker(bind=self.engine)
                    session = curr_session()
                    query = SQLUtils.show_cart_wo_login(table_name, sql_model["session_id"])
                    logging.info("query %s",query)
                    cart_list = []
                    response = session.execute(text(query))
                    session.close()
                    logging.info("session closed")
                    for res in response:
                        print(res)
                        cart_list.append(res)
                    return HelperUtils.tupple_to_dict(cart_list,["session_id","cart_id", "item_id", "count","is_active"])
            except OperationalError as e:
                logging.error("Error: connection issue {}".format(e))
                retries += 1
                print("in loop")
                time.sleep(1)
            except Exception as ex:
                logging.error("An exception occurred:{}".format(ex))
                raise ex

        raise Exception("Could not perform database eration after {} retries".format(max_retries))


sql_client = SQLClient()



