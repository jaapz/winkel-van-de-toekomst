from app import db

shopping_lists_to_products = db.Table(
    'shopping_lists_to_products',
    db.Model.metadata,
    db.Column('shopping_list_id', db.Integer, db.ForeignKey('shopping_list.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)


class Product(db.Model):
    """ Represents a real-life Product that the shop sells. """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    barcode = db.Column(db.String(100))


class ShoppingList(db.Model):
    """ Represents a shopping list containing several products. """
    __tablename__ = 'shopping_list'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    products = db.relationship(Product, secondary=shopping_lists_to_products,
                               backref='shopping_lists')
