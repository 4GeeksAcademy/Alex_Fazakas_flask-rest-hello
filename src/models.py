from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    birth_year = db.Column(db.String(50))
    gender = db.Column(db.Enum('male', 'female', 'other', name = 'gender'), nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    eye_color = db.Column(db.Enum('blue', 'brown', 'green', 'black', 'other', name='eyes'), nullable=False)
    hair_color = db.Column(db.Enum('blond', 'brown', 'ginger', 'black', 'other', name = 'hair'), nullable=False)  
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    #planet = db.relationship(Planet)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'gender': self.gender,
            'height': self.height,
            'weight' : self.weight,
            'eyes': self.eye_color,
            'hair': self.hair_color,
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    diameter = db.Column(db.Integer)
    climate = db.Column(db.Enum('temperate', 'tropical', 'arid', 'frozen', 'murky', name = 'climate'))
    terrain = db.Column(db.Enum('jungle, rainforests', 'grasslands, mountains', 'ocean', 'desert', 'tundra', 'ice caves, mountain ranges', 'forests, mountains, lakes', 'swamp, jungles', 'other', name = 'terrain'))
    surface_water = db.Column(db.Integer)
    population = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    gravity = db.Column(db.String(50))
   
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'diameter': self.diameter,
            'climate': self.climate,
            'terrain': self.terrain,
            'surface_water' : self.surface_water,
            'population': self.population,
            'orbital_period': self.orbital_period,
            'rotation_period': self.rotation_period,
            'gravity' : self.gravity,
        }

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    model = db.Column(db.String(100))
    length = db.Column(db.Integer)
    cargo = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    manufacturer = db.Column(db.Enum('Corellia Mining Corporation', 'SoroSuub Corporation', 'Incom Corporation', 'Sienar Fleet Systems', ' Ubrikkian Industries', name='manufacturer'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id')) 
    character = db.relationship(Character)
      
    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'length': self.length,
            'cargo': self.cargo,
            'speed': self.speed,
            'crew': self.crew,
            'passengers': self.passengers,
            'manufacturer': self.manufacturer,
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship(Character)

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)
    
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle = db.relationship(Vehicle)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            'id': self.id
        }
    