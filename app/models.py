from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    functions = db.Column(db.String(2048 * 64))
    operators = db.Column(db.String(256 * 64))
    tokens = db.relationship('Token', backref='owner', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Token(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    expires_in = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Token {self.id} of user {self.user_id}>'
