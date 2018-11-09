from db import db # db = SQLAlchemy()


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    """SQLAlchemy is smart enough to be able to construct a many-to-one relationship 
    from this. Every item has a store_id property, 
    so the items property of the StoreModel becomes a list of those items.
    Or at least, it would if we remove lazy="dynamic".
    With lazy="dynamic", items becomes a SQLAlchemy query, 
    so whenever we want to access the items in the store we have to do something like this:
    store.items.all(), .all() is the key part here, and only needed when lazy="dynamic
    If we take away lazy="dynamic", then the items are loaded from the database 
    as soon as the StoreModel object is created."""
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # using all() to retrieve all items from that store table
        return {
                'id': self.id,
                'name': self.name,
                'items': [item.json() for item in self.items.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        # SQLAlchemy can convert object to row of database
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
