from wt_cart.application import app
from waitress import serve
import logging


if __name__ == "__main__":

    print("starting...")
    logging.basicConfig(filename='cart.log',level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    serve(app,host="0.0.0.0",port=5008)