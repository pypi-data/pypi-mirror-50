from typing import List

from pysubway.model import db


class Product(db.Model):
    __tablename__ = 'product'
    __bind_key__ = 'guard'

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(100), nullable=False, unique=True)
    mode = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(100, u'utf8_bin'), nullable=False)
    description = db.Column(db.String(255, u'utf8_bin'), nullable=False)
    path = db.Column(db.String(100, u'utf8_bin'))
    user_id = db.Column(db.ForeignKey(u'user.id'), nullable=False, index=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    delete_at = db.Column(db.DateTime)

    @classmethod
    def get_all(cls) -> List['Product']:
        return cls.query.all()
