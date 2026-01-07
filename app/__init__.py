from flask import Flask
from app.extension import db,migrate,ma,limiter
from config.cors import CORS_CONFIG
from flask_cors import CORS
from config.logging import setup_logging
from flask_jwt_extended import JWTManager
from config.database import DatabaseConfig
from config.jwt import JWTConfig
from app.exceptions.handler import register_error_handlers

app = Flask(__name__)

#///// implement log ///////////////
setup_logging(app)

# ///// implement cors /////////////////
CORS(app, **CORS_CONFIG)

# ///// setup database and jwt ///////////////////
app.config.from_object(DatabaseConfig)
app.config.from_object(JWTConfig)

# /////// Initialize extensions ////////////
db.init_app(app)
migrate.init_app(app, db)
limiter.init_app(app)
ma.init_app(app)

# JWT
jwt = JWTManager(app)

# /////// implement models ////////////////
from app.models import *

# ///////////////// implement web /////////
import route.api as routes
# register all Blueprint Route
for bp_name in getattr(routes, "__all__", []):
    bp = getattr(routes, bp_name)
    app.register_blueprint(bp)

# //////// register error handler /////////
register_error_handlers(app)

# //////// run application ////////////////
if __name__ == '__main__':
    app.run(debug=True)