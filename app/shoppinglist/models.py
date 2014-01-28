from app import db


class ShoppingListToProduct(db.Model):
    """ Maps the many-to-many of ShoppingLists and Products. """
    __tablename__ = 'shopping_lists_to_products'

    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'),
                                 primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           primary_key=True)

    product = db.relationship('Product')
    shopping_list = db.relationship('ShoppingList')

    # The amount that is added in the website.
    amount = db.Column(db.Integer)

    # The amount that is actually scanned in the shop.
    amount_scanned = db.Column(db.Integer)


class Product(db.Model):
    """ Represents a real-life Product that the shop sells. """
    __tablename__ = 'product'

    # ID doubles as the barcode
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    shopping_lists = db.relationship(ShoppingListToProduct)

    def get_shopping_list_assocation(self, shopping_list):
        for assoc in self.shopping_lists:
            if assoc.shopping_list.id == shopping_list.id:
                return assoc

        return None

    def to_dict(self, shopping_list=None):
        result = dict(
            id=self.id,
            name=self.name,
            price=self.price
        )

        # Is a shopping list if provided, also get the amount and
        # amount_scanned
        if shopping_list is not None:
            association = self.get_shopping_list_assocation(shopping_list)
            result.update(dict(
                amount=association.amount,
                amount_scanned=association.amount_scanned
            ))

        return result


class ShoppingList(db.Model):
    """ Represents a shopping list containing several products. """
    __tablename__ = 'shopping_list'

    STATUSSES = ['niet betaald', 'in behandeling', 'betaald']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    products = db.relationship(ShoppingListToProduct)

    @property
    def nice_status(self):
        return ShoppingList.STATUSSES[self.status]

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            user_id=self.user.id if self.user else None,
            products=[p.product.to_dict(self) for p in self.products]
        )
