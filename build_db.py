import os
from config import db
from models import Item, ItemSchema

# Data to initialize database with
items = [
    {"id": 0, "name":"first item"}, 
    {"id": 1, "name":"second item"}
]

# Delete database file if it exists currently
if os.path.exists("items.db"):
    os.remove("items.db")

# Create the database
db.create_all()

# iterate over the item structure and populate the database
for element in items:
    print(element['name'])
    item = Item(id = element['id'], name=element['name'])
    db.session.add(item)

db.session.commit()

# let's check does items are in database
# Create the list of items from database

items = Item.query.order_by(Item.name).all()

# Serialize the data for the response
item_schema = ItemSchema(many=True)
data = item_schema.dump(items)

print(data)