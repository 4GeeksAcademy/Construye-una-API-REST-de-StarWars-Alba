from app import app, db
from models import Users, People, Planets, Favorites

with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = Users (name="albacete", lastname="diaz", email="albacete@example.com", password="1234",  gender="FEMALE")
    user2 = Users (name="alba", lastname="lopez", email="alba@example.com", password="5678",  gender="FEMALE")
   
    db.session.add_all([user1, user2])
    db.session.commit()
  
    # profile1 = Profiles(bio="Soy Albacete", user_id=user1.id)
    # profile2 = Profiles(bio="Soy Alba", user_id=user2.id)

    # db.session.add_all([profile1, profile2])
    # db.session.commit()

 
    #Planets
    planet1 = Planets(planet_name="Home", population=76876, climate="Dry", diameter=234, gravity=32344, films="A new Hope")
    planet2 = Planets(planet_name="Homeneu", population=6876, climate="Humid", diameter=2344, gravity=744, films="A new Pope")
    db.session.add_all([planet1, planet2])
    db.session.commit()

    #People
    people1 = People(character_name="Luke Skywalker", birth_year="19 BBY", gender="Male", hair_color="Blond", height=77, films="A New Hope", vehicles="Snowspeeder", planet_id=planet1.id)
    people2 = People(character_name="Luke Skywalkerina", birth_year="09 BBY", gender="Female", hair_color="Black", height=87, films="A New Pope", vehicles="Motomami", planet_id=planet2.id)
    db.session.add_all([people1, people2])

    #Favorites
    favorite1 = Favorites(user_id=user1.id, people_id=people1.id, planets_id=planet1.id)
    favorite2 = Favorites(user_id=user2.id, people_id=people2.id, planets_id=planet2.id)
    db.session.add_all([favorite1, favorite2])
    db.session.commit()

    print("✅ Datos sembrados correctamente.")

