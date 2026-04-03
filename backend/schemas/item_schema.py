from apiflask import Schema
from apiflask.fields import String, Integer, List, Nested


class ItemSchema(Schema):
    id = Integer()
    name = String()

class ItemsOutSchema(Schema):
    items = List(ItemSchema())
