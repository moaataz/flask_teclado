from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import ItemSchema,ItemUpdateSchema
from models import ItemModel
from db import db
from flask_jwt_extended import jwt_required,get_jwt
from sqlalchemy.exc import SQLAlchemyError

blp = Blueprint('Items',__name__,description="operations on stores")

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    @jwt_required()
    def delete(self,item_id):
        jwt = get_jwt()
        if not get_jwt('is_admin'):
            abort(401,'admin privilege required')
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message':'item deleted'}
        
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id,**item_data)
        db.session.add(item)
        db.session.commit()
        return item
        # try:
        #     item = items[item_id]
        #     item |= item_data
        #     return item
        # except KeyError:
        #     abort(404,message="item not found")

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as exc:
            print(exc)
            abort(500,message='an error occured whilst inserting the item')
        
        return item