import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def find_isexist(artist, album):
    """
    Проверяет наличие альбома в базе по исполнителю и альбому
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).filter(Album.album == album).all()
    if albums:
        return True
    else:
        return False


def save(new_album_data):
    """
    Записывает новый альбом в базу
    """
    new_album = Album(
        year=new_album_data["year"],
        artist=new_album_data["artist"],
        genre=new_album_data["genre"],
        album=new_album_data["album"]
    )
    session = connect_db()
    session.add(new_album)
    session.commit()
    print("Данные сохранены!")
