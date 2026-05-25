import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    
    # Relación bidireccional para acceder a los favoritos desde el usuario
    favorites = relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
            # Nunca serializar el password por seguridad
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)  # Puede ser null si el favorito es un personaje
    character_id: Mapped[int] = mapped_column(ForeignKey('character.id'), nullable=True)  # Puede ser null si el favorito es un planeta

    # Relaciones para que SQLAlchemy y eralchemy entiendan las conexiones
    user = relationship('User', back_populates='favorites')
    planet = relationship('Planet')
    character = relationship('Character')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }

# Bloque obligatorio al final para generar el diagrama con el nuevo estándar
if __name__ == '__main__':
    from eralchemy2 import render_er
    try:
        # Usamos db.metadata para que el diagrama dependa correctamente de la estructura de Flask
        render_er(db.metadata, 'diagram.png')
        print("¡Éxito! El archivo diagram.png de Star Wars se ha generado correctamente.")
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")