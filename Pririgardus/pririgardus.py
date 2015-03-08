#pririgardus.py
import os
import logging
import argparse
from flask import (Flask)
from models.models import db

NOMBRE_BASE_DATOS = 'pririgardus.db'
app = Flask(__name__)
app.config["STATIC_URL"] = '/static/'
app.config["STATIC_ROOT"] = '/static/'
app.config["BASE_DIR"] = os.path.dirname(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + NOMBRE_BASE_DATOS
db.init_app(app)
db.app = app

parser = argparse.ArgumentParser(description='Pririgardus Arguments Parser')
parser.add_argument('-l', '--logging', help='logging', action='store_true')
parser.add_argument('-d', '--debug', help='debug', action='store_true')
parser.add_argument('-p', '--port', help='port', type=int, default=5000)
argv = parser.parse_args()

logger = logging.getLogger('PRG')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if(argv.logging):
    logger.addHandler(handler)


if __name__ == "__main__":
    debugging = argv.debug
    port = int(os.environ.get("PORT", argv.port))
    try:
        app.run(host='0.0.0.0', port=port, debug=debugging)
    except OSError as ose:
        print(
            "Port in use, select another using -p [port] but {0}".format(
                argv.port))
        print("Maybe you press Ctrl+Z to stop the server...only you know that")
