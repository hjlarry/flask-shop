from elasticsearch_dsl import Boolean, Document, Integer, Float, Date
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=ES_HOSTS)


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
