from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
    nombre = db.Column(db.String(50), nullable=False )
    genero = db.Column(db.Enum('masculino','femenino', name='Genero'), nullable=False)
    hair_color = db.Column(db.Enum('negro','rubio', name='HairColor'), nullable=False)
    eye_color = db.Column(db.Enum('verdes','azules', name='EyeColor'), nullable=False)
    def __repr__(self):
        return '<Character %r>' % self.nombre
    def serialize(self): #aca va todos lo que este en class libro
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True) # nombre agregar
    population = db.Column(db.Integer, nullable=False)
    terrain = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Planet %r>' % self.id
    def serialize(self): #aca va todos lo que este en class libro
        return {
            "id": self.id,
            "population": self.population,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }
class Favorito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planetId = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)
    characterId = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=True)
    
    def __repr__(self):
        return '<Favorito %r>' % self.id
    
    def serialize(self):  
        return {
            "id": self.id,
            "planetId": self.planetId,
            "characterId": self.characterId
        }