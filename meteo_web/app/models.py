from app import db

class datasources(db.Model):
    __tablename__ = 'datasources'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    meteostation_id = db.Column(db.Integer, db.ForeignKey('meteostations.id'), nullable=False)
    datasource_url = db.Column(db.String(255), nullable=False)
    processed_datetime = db.Column(db.String(50), nullable=True)


class meteostations(db.Model):
    __tablename__ = 'meteostations'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    region = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    longtitude = db.Column(db.Float, nullable=True)
    latitutde = db.Column(db.Float, nullable=True)

    # Relationships with other tables
    datasources = db.relationship('datasources', backref='datas', lazy=True)
    temperatures = db.relationship('temperature', backref='temp', lazy=True)


class temperature(db.Model):
    __tablename__ = 'temperatures'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    meteostation_id = db.Column(db.Integer, db.ForeignKey('meteostations.id'), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    temperature = db.Column(db.Float, nullable=False)


