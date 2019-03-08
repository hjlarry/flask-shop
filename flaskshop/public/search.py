from elasticsearch_dsl import Boolean, Document, Integer, Float, Date, Text
from elasticsearch_dsl.connections import connections
from flask_sqlalchemy import Pagination

from flaskshop.settings import Config
from flaskshop.product.models import Product

connections.create_connection(hosts=Config.ES_HOSTS)

SERACH_FIELDS = ["title^10", "description^5"]


def get_item_data(item):
    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "first_img": item.first_img,
        "basic_price": item.basic_price,
        "price": item.price,
        "on_sale": item.on_sale,
        "is_discounted": item.is_discounted,
    }


class Item(Document):
    id = Integer()
    title = Text()
    description = Text()
    first_img = Text()
    basic_price = Float()
    price = Float()
    on_sale = Boolean()
    is_discounted = Boolean()
    created_at = Date()

    @classmethod
    def get(cls, id):
        return super().get(id)

    @classmethod
    def add(cls, item):
        obj = cls(**get_item_data(item))
        obj.save()
        return obj

    @classmethod
    def update_item(cls, item):
        obj = cls.get(item.id)
        if obj is None:
            return cls.add(obj)
        if not obj:
            return
        kw = get_item_data(item)
        try:
            obj.update(**kw)
        except ConflictError:
            obj = cls.get(item.id)
            obj.update(**kw)
        return True

    @classmethod
    def get_es(cls):
        search = cls.search()
        return connections.get_connection(search._using)

    @classmethod
    def new_search(cls, query, page, order_by=None, per_page=16):
        s = cls.search()
        s = s.query("multi_match", query=query, fields=SERACH_FIELDS)
        start = (page - 1) * per_page
        s = s.extra(**{"from": start, "size": per_page})
        s = s if order_by is None else s.sort(order_by)
        rs = s.execute()
        print(rs)
        items = []
        return Pagination(query, page, per_page, rs.hits.total, items)
