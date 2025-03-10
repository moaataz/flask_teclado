import uuid
from flask_smorest import abort
from flask import Flask,request
from db import stores,items

app = Flask(__name__)


@app.get('/store')
def get_stores():
    return {'stores':list(stores.values())}

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {'message':'store not found'},404

@app.post('/store')
def create_store():
    store_data = request.get_json()
    if 'name' not in store_data:
        abort(
            400,message='bad request, ensure \'name\' is included in json payload'
        )
    for store in stores.values():
        if store_data['name'] == store['name']:
            abort(400,message='store already exists')
    store_id = uuid.uuid4().hex
    store = {**store_data,'id':store_id}
    stores[store_id] = store
    return store,201
@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message':'item deleted succsesfully'},201
    except KeyError:
        return abort(404,message='item not found')
@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
        'price' not in item_data or
        'name' not in item_data or
        'store_id' not in item_data
    ):
        abort(400,message="bad request, ensure 'store', 'price', 'name' are included in json payload")
    if item_data['store_id'] not in stores:
        return abort(404,message='store not found')
    for item in items.values():
        if (item_data['name'] == item['name'] and item_data['store_id'] == item['store_id']):
            abort(400,'item is already exists')
    item_id = uuid.uuid4().hex
    item = {**item_data,'id':item_id}
    items[item_id] = item
    return item,201


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404,message='item not found')
    
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {'message':'item deleted succsesfully'},201
    except KeyError:
        return abort(404,message='item not found')
@app.put('/item/<string:item_id>')
def update_item(item_id):
    item_data = request.get_json()
    if 'price' not in item_data or 'name' not in item_data:
        abort(400,'bad request, ensure \'price\' and \'name\' are included in json payload')
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404,message="item not found")
    
if __name__ == "__main__":
    app.run(debug=True)