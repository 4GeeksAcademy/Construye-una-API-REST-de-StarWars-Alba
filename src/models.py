from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as sqlalchemyEnum
from enum import Enum

db = SQLAlchemy()


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(sqlalchemyEnum(
        GenderEnum, name="genderenum"), nullable=True)  # esto tampoco estoy segura

    # profile: Mapped["Profiles"] = relationship(
    #     back_populates="user", uselist=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            "gender": self.gender.value if self.gender else None,

            # "profile": self.profile.serialize() if self.profile else None,
            # "favorites": [favorite.serialize() for favorite in self.favorites]
        }


# class Profiles(db.Model):
#     __tablename__ = "profiles"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     # aqui no hace falta el nullable=False verdad?
#     bio: Mapped[str] = mapped_column(String(2000))

#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     user: Mapped["Users"] = relationship(back_populates="profile")

#     def serialize(self):  # que criterio a seguir para incluir en el serialize? que es lo que quiero que se reciba?
#         return {
#             "id": self.id,
#             "bio": self.bio,
#             "user_id": self.user_id,
#             # aqui no estoy segura de que tengo que poner, si lleva serialize o no
#             "user": self.user.serialize() if self.user else None,
#         }


class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)

    character_name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[int] = mapped_column(nullable=False)
    films: Mapped[str] = mapped_column(String(10000), nullable=False)
    vehicles: Mapped[str] = mapped_column(String(50), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship(
        back_populates="people")
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))
    # uselist=False --> aqui va el uselist para que no lo devuelva en lista? porque es solo un planeta?
    planet: Mapped["Planets"] = relationship(back_populates="people")

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "films": self.films,
            "vehicles": self.vehicles,

            # "favorites": [favorite.serialize() for favorite in self.favorites],
            # "planet_id": self.planet_id.serialize() if self.planet_id else None,
            # "planet": self.planet.serialize() if self.planet else None
        }


class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    planet_name: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    gravity: Mapped[int] = mapped_column(nullable=False)
    films: Mapped[str] = mapped_column(String(50000), nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship(
        back_populates="planets")
    people: Mapped[list["People"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "films": self.films,

            "favorites": [favorite.serialize() for favorite in self.favorites],
            # esto está bien o debería cambiar people y poner p?
            "people": [character.serialize() for character in self.people]

        }


class Favorites(db.Model):
    __tablename__ = "favorites"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    people_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"), primary_key=True)
    planets_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), primary_key=True)

    user: Mapped["Users"] = relationship(back_populates="favorites")
    people: Mapped["People"] = relationship(back_populates="favorites")
    planets: Mapped["Planets"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planets_id": self.planets_id,

            "user": self.user.serialize() if self.user else None,
            "people": self.people.serialize() if self.people else None,
            "planets": self.planets.serialize() if self.planets else None
        }
