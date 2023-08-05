from pysubway.model import db


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(32, u'utf8_bin'), nullable=False, unique=True)
    chinese_name = db.Column(db.String(32, u'utf8_bin'), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)
    remark = db.Column(db.String(200, u'utf8_bin'), nullable=False)
    update_at = db.Column(db.DateTime, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
