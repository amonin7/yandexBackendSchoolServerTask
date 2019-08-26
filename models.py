from app import db

class Citizen(db.Model):
    __tablename__ = 'citizens'

    id = db.Column(db.Integer, primary_key=True)
    import_id = db.Column(db.Integer)
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String())
    street = db.Column(db.String())
    building = db.Column(db.String())
    apartment = db.Column(db.Integer)
    name = db.Column(db.String())
    birth_date = db.Column(db.String())
    gender = db.Column(db.String())
    relatives = db.Column(db.String())

    def __init__(self, import_id, citizen_id, town, street, building, apartment, name, birth_date, gender, relatives):
        self.import_id = import_id
        self.citizen_id = citizen_id
        self.town = town
        self.street = street
        self.building = building
        self.apartment = apartment
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.relatives = relatives

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'import_id': self.import_id,
            'citizen_id': self.citizen_id,
            'town': self.town,
            'street': self.street,
            'building': self.building,
            'apartment': self.apartment,
            'name': self.name,
            'birth_date': self.birth_date,
            'gender': self.gender,
            'relatives': list(map(int, self.relatives.split()))
        }
