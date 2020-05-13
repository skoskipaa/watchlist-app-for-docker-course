from application import db


class Watchlist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    name = db.Column(db.String(200), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    content = db.relationship("Content", backref='watchlist', lazy=True)


    def __init__(self, name):
        self.name = name

    