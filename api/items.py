from connexion import NoContent
from flask import jsonify, abort, make_response
from models import Item, ItemSchema
from config import db
import logging

def get_all():

    items = Item.query.order_by(Item.id).all()

    return ItemSchema(many=True).dump(items)

def get_by_id(item_id):

    item = Item.query.filter(Item.id == item_id).one_or_none()

    if item is not None:

        item_schema = ItemSchema()
        data = item_schema.dump(item)
        return data

    else:
        abort(
            404,
            "Item not found for Id: {item_id}".format(item_id=item_id),
        )
    
def insert(item):

    print("insert")
    id = item['id']
    name = item['name']

    existing_item = (
        Item.query.filter(Item.id == id)
        .filter(Item.name == name)
        .one_or_none()
    )

    if existing_item is None:

        schema = ItemSchema()
        new_item= schema.load(item, session=db.session)

        db.session.add(new_item)
        db.session.commit()

        data = schema.dump(new_item)

        return data, 201

    else:
        abort(
            409,
            "Item id:{id}, name:{name} exists already".format(
                id=id, name=name
            ),
        )

def delete(item_id):
    
    item = Item.query.filter(Item.id == item_id).one_or_none()

    if item is not None:
        
        db.session.delete(item)
        db.session.commit()
        return make_response(
            "Item {item_id} deleted".format(item_id=item_id), 200
        )
    else:
        abort(
            404,
            "Item not found for Id: {item_id}".format(item_id=item_id),
        )

def update(item_id, item):

    id = item['id']
    name = item['name']

    existing_item = (
        Item.query.filter(Item.id == id)
        .one_or_none()
    )

    if existing_item is None:
        abort(
            404,
            "Item not found for Id: {item_id}".format(item_id=item_id),
        )
    else:

        schema = ItemSchema()
        updated_item = schema.load(item, session=db.session)

        updated_item.id = existing_item.id

        db.session.merge(updated_item)
        db.session.commit()

        data = schema.dump(updated_item)

        return data, 200



