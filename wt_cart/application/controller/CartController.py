import logging,json
from http import HTTPStatus
from dataclasses import asdict
from flask import jsonify, make_response,request
from wt_cart.application.model.Error import Error
from wt_cart.application.model.SqlModel import SqlModel
from wt_cart.application.model.InventoryModel import InventoryModel
from wt_cart.application.service.SQLOrmService import SQLOrmService,sql_service
from wt_cart.application.service.JWTClient import JWTClient,jwt_client
from wt_cart.application.service.FirebaseJwtClient import firebase_jwt_client
from wt_cart.application import app

logging.getLogger().setLevel(logging.INFO)


class CartController:
    def __init__(self,s: SQLOrmService):
        self.service = s


cart_controller = CartController(sql_service)


@app.get('/')
def welcome():
    return "Welcome to service"

def cors_preflight():
    # Respond to the OPTIONS preflight request with the necessary CORS headers
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')

    return response

# Handle the OPTIONS request for /sign_in/ separately
app.add_url_rule('/add_wo_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/add_with_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/update_wo_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/remove_wo_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/show_wo_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/show_with_login', view_func=cors_preflight, methods=['OPTIONS'])
app.add_url_rule('/checkout_with_login', view_func=cors_preflight, methods=['OPTIONS'])


@app.post('/add_wo_login',endpoint='add_to_cart_wo_login')
@jwt_client.jwt_required
def add_to_cart_wo_login(session_id):
    if not session_id:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    else:
        try:
            item_id = request.json['item_id']
            count = request.json['count']
            is_active = request.json['is_active']
            cart_model = asdict(SqlModel(session_id, session_id, item_id, count, is_active))
            inventory_model=asdict(InventoryModel(item_id))
            response=cart_controller.service.add_to_cart(cart_model,inventory_model)
            if response:
                return f"Response received.{response}"
            else:
                logging.error("No response found. Internal Error.")
        except Exception as ex:
            logging.error(ex)


@app.post('/add_with_login',endpoint='add_to_cart_with_login')
@firebase_jwt_client.jwt_required
def add_to_cart_with_login(response):
    if not response:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    else:
        try:
            print(response)
            item_id = request.json['item_id']
            count = request.json['count']
            is_active = request.json['is_active']
            cart_model = asdict(SqlModel(response['session_id'],response['session_id'], item_id, count, is_active))
            inventory_model=asdict(InventoryModel(item_id))
            response=cart_controller.service.add_to_cart(cart_model,inventory_model)
            if response:
                return f"Response received.{response}"
            else:
                logging.error("No response found. Internal Error.")
        except Exception as ex:
            logging.error(ex)


@app.post('/update_wo_login',endpoint='update_to_cart_wo_login')
#@jwt_client.jwt_required
def update_to_cart_wo_login():
    try:
        session_id = request.json['session_id']
        item_id = request.json['item_id']
        count = request.json['count']
        is_active = request.json['is_active']
        cart_model = asdict(SqlModel(session_id, session_id, item_id, count, is_active))
        inventory_model=asdict(InventoryModel(item_id))
        response=cart_controller.service.update_to_cart(cart_model,inventory_model)
        if response:
            return f"Response received.{response}"
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)


@app.post('/remove_wo_login',endpoint='remove_from_cart_wo_login')
#@jwt_client.jwt_required
def remove_from_cart_wo_login():
    try:
        session_id = request.json['session_id']
        item_id = request.json['item_id']
        count = request.json['count']
        is_active = request.json['is_active']
        cart_model = asdict(SqlModel(session_id,session_id, item_id, count, is_active))
        logging.info("jjjjj",cart_model)
        response = cart_controller.service.remove_from_cart(cart_model)
        if response:
            return f"Response received.{response}"
        else:
            logging.error("No response found. Internal Error.")
    except Exception as ex:
        logging.error(ex)


@app.post('/show_wo_login',endpoint='show_from_cart_wo_login')
@jwt_client.jwt_required
def show_from_cart_wo_login(session_id):
    if not session_id:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    else:
        try:
            item_id = request.json['item_id']
            count = request.json['count']
            is_active = request.json['is_active']
            cart_model = asdict(SqlModel(session_id,session_id, item_id, count, is_active))
            print("ggggg",cart_model)
            response=cart_controller.service.show_cart_with_session(cart_model)
            if len(response) > 0:
                return jsonify(response,200)
            else:
                error = Error(message="no session_id present", type=404, message_id=HTTPStatus.BAD_REQUEST)
                return make_response(jsonify(error, HTTPStatus.BAD_REQUEST))

        except Exception as ex:
            logging.error(ex)

@app.post('/show_with_login',endpoint='show_from_cart_with_login')
@firebase_jwt_client.jwt_required
def show_from_cart_with_login(response):
    if not response:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    else:
        try:
            logging.info(response)
            item_id = request.json['item_id']
            count = request.json['count']
            is_active = request.json['is_active']
            cart_model = asdict(SqlModel(response['session_id'],response['session_id'], item_id, count, is_active))
            response=cart_controller.service.show_cart_with_login(cart_model,response['user_id'])
            logging.info(response)
            if len(response) > 0:
                return jsonify(response,200)
            else:
                error = Error(message="no session_id present", type=404, message_id=HTTPStatus.BAD_REQUEST)
                return make_response(jsonify(error, HTTPStatus.BAD_REQUEST))

        except Exception as ex:
            logging.error(ex)

@app.post('/checkout_with_login',endpoint='checkout_from_cart_with_login')
@firebase_jwt_client.jwt_required
def checkout_from_cart_with_login(response):
    if not response:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    else:
        try:
            logging.info(response)
            item_id = request.json['item_id']
            count = request.json['count']
            is_active = request.json['is_active']
            discount_code = request.json['discount_code']
            cart_model = asdict(SqlModel(response['session_id'],response['session_id'], item_id, count, is_active))
            response=cart_controller.service.check_out_with_login(cart_model,response['user_id'],discount_code)
            logging.info(response)
            if not response:
                return jsonify("no cart item found")
            if len(response) > 0:
                return jsonify(response,200)
            else:
                error = Error(message="no item present", type=404, message_id=HTTPStatus.BAD_REQUEST)
                return make_response(jsonify(error, HTTPStatus.BAD_REQUEST))

        except Exception as ex:
            logging.error(ex)



