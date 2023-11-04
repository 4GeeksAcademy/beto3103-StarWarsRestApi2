from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(80), nullable = False, unique = True)
	password = db.Column(db.String(20), nullable = False, unique = False)
	email = db.Column(db.String(50), nullable = False, unique = False)
	
	#RELATIONSHIP
	favorite = db.relationship("Favorite", uselist = True, backref = "User")
	
	#FUNCTIONS
	def __repr__(self):
		return '<User %r>' % self.name #preguntar que es el %

	def serialize(self):
		return {
			"id":self.id,
			"username":self.username,
			"email":self.email,
            "favorites" : list(map(lambda item: item.serialize(), self.favorite))
		}

class People(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), nullable = False)
	birth_year = db.Column(db.String(10), nullable = False) # validar como viaja en SWAPI
	eye_color = db.Column(db.String(10), nullable = False)
	gender = db.Column(db.String(10), nullable = False)
	hair_color = db.Column(db.String(10), nullable = False)
	height = db.Column(db.Integer())
	mass = db.Column(db.Integer())
	skin_color = db.Column(db.String(10))
	#RELATIONSHIP
	favorite = db.relationship("Favorite", uselist= True, backref = "people")

	#FUNCTIONS
	def __repr__(self):
		return '<People %r>' % self.name #preguntar que es el %

	def serialize(self):
		return {
			"id":self.id,
			"name":self.name,
			"eye_color":self.eye_color,
			"gender": self.gender,
		}

class Planet(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String(80), nullable = False)
	climate = db.Column(db.String(40))
	created = db.Column(db.DateTime())
	diameter = db.Column(db.Integer())
	edited = db.Column(db.DateTime())
	gravity = db.Column(db.Integer())
	orbital_period = db.Column(db.Integer())
	population = db.Column(db.Integer())
	rotation_period = db.Column(db.Integer())
	surface_water = db.Column(db.Integer())
	terrain = db.Column(db.String(40))
	#RELATIONSHIP
	favorite = db.relationship("Favorite", uselist = True, backref = "planet")

	#FUNCTIONS
	def __repr__(self):
		return '<Planet %r>' % self.name #preguntar que es el %

	def serialize(self):
		return {
			"id":self.id,
			"climate":self.climate,
			"population":self.population,
		}

class Favorite(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	#RELATIONSHIP	
	user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
	people_id = db.Column(db.Integer(), db.ForeignKey("people.id"))
	planet_id = db.Column(db.Integer(), db.ForeignKey("planet.id"))

	#FUNCTIONS
	def __repr__(self):
		return '<Favorite %r>' % self.name #preguntar que es el %

	def serialize(self):
		return {
			"id":self.id,
			"user_id":self.user_id,
			"people_id":self.people_id,
			"planet_id":self.planet_id,
		}


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }