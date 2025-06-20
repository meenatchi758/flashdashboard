from extensions import db

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    total = db.Column(db.Float)
