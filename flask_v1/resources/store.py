from flask_restful import Resource  
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store: 
            return store.json()
        return {'message': "Store not found"}, 404
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store already exists"}, 400
        
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occured while save the store"}, 500
        
        return store.json(), 201
    
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {"message": "Store not found"}, 404

        store.delete_from_db()

        return {"message":"A store deleted"}, 201


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}