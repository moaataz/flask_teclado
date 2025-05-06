from flask import Flask,jsonify
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint
from db import db
from block_list import BLOCKLIST
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
import secrets

import models
def create_app(databaseUrl=None):

    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = False
    app.config['API_TITLE'] = 'flask rest apis'
    app.config['API_VERSION'] = '3.0.3'
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['SQLALCHEMY_DATABASE_URI'] = databaseUrl or os.getenv('DATABASE_URL','sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
    db.init_app(app)
    migrate = Migrate(app,db)
    api = Api(app)
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = "314018678676033960458934045265980507753"
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == '1':
            return {'is_admin':True}
        return {'is_admin':False}
    @jwt.token_in_blocklist_loader
    def logged_out_users(jwt_header,jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return jsonify({"description":"the token has been revoked","error":'token_revoked'},401)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)
    return app