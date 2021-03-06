from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from datetime import date

import albums


# пользовательский класс исключений
class WrongYear(ValueError):
    pass


@route("/albums/<artist>")
def find_albums(artist):
    albums_list = albums.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list if album.album is not None]    #проверка на случай, если в базе дефектная строка без названия альбома
        result = "У исполнителя {} найдено {} альбомов.<br>".format(artist, len(album_names))
        result += "Список альбомов:<br>".format(artist)
        result += "<br>".join(album_names)
    return result


@route("/albums", method="POST")
def save_album():
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album = request.forms.get("album")
    year = request.forms.get("year")
    """
    Проверка наличия всех требуемых параметров (исключить None и пустую строку) 
    """
    new_album = {
        "artist": artist,
        "genre": genre,
        "album": album,
        "year": year
    }

    empty = [None, ""]
    absent_parameters_list =[]
    for key, value in new_album.items():
        if value in empty:
            absent_parameters_list.append(key)
    if absent_parameters_list:
        absent_parameters = ", ".join(absent_parameters_list)
        message = "Некоторые параметры не заданы: {}.".format(absent_parameters)
        err400 = HTTPError(400, message)
        return err400

    """
    Проверка корректности параметра "год". Остальные параметры будут по-любому или строки, или None. На None уже проверили.
    """
    try:
        year_int = int(year)
        if year_int < 1893 or year_int > date.today().year:
            raise WrongYear("Год выпуска альбома не может быть {}".format(year_int))
    except WrongYear as w_e:
        err400 = HTTPError(400, w_e)
        return err400
    except ValueError:
        message = 'Параметр "year" не может быть преобразован в число'
        err400 = HTTPError(400, message)
        return err400
    else:
        new_album[year] = year_int

    """
    Проверка наличия альбома в базе
    """
    if albums.find_isexist(artist, album):
        message = "Альбом {} - {} уже есть в базе".format(artist, album)
        err409 = HTTPError(409, message)
        return err409

    """
    Запись в базу
    """
    albums.save(new_album)
    return "Данные успешно сохранены"


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)


#  http -f GET http://localhost:8080/albums/"Pink Floyd"
#  http -f POST http://localhost:8080/albums artist="New Artist" genre="Rock" album="Super" year="1987"
