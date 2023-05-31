from istorage import IStorage
import json
import requests
from colorama import Fore

class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def api(self, movie_name):
        apy_key = "26e330a6&t"
        name_movie = movie_name
        url = f"https://www.omdbapi.com/?apikey={apy_key}={name_movie}"
        res = requests.get(url)
        res = res.json()
        return res

    def country_flag(self, country_name):
        url = f"https://cdn.jsdelivr.net/npm/country-flag-emoji-json@2.0.0/dist/index.json"
        res = requests.get(url)
        res = res.json()
        image = ''
        for country in res:
            if country["name"] == country_name:
                image = country["image"]
        return image

    def list_movies(self):
        with open(self.file_path, "r") as file:
            movies = json.loads(file.read())
        return movies

    def add_movie(self, name):
        movie_json = self.api(name)
        if movie_json.get('Error'):
            print(f"Movie {name} not found!")
            return False
        name = movie_json['Title']
        year = movie_json['Year']
        rating = movie_json['imdbRating']
        postr = movie_json['Poster']
        imdb_id = movie_json['imdbID']
        country = movie_json['Country']
        with open(self.file_path, "r") as file:
            movies = json.loads(file.read())
        movie_dict = {'name': name, 'rating': rating, 'year': year, 'Poster': postr, 'imdb_id': imdb_id,
                      'Country': country}
        movies.append(movie_dict)
        with open(self.file_path, "w") as file:
            json.dump(movies, file)
        print(f"Movie {name} was successfully added")
        return True

    def delete_movie(self, name):
        flag = True
        with open(self.file_path, "r") as file:
            movies = json.loads(file.read())
        answer = ''
        for movie in movies:
            if name.lower() == movie["name"].lower():
                movies.remove(movie)
                answer = f"Movie {movie['name']} successfully deleted"
                flag = True
                break
            else:
                answer = Fore.RED + f"Movie {name} doesn't exist!"
                flag = False
        print(answer)
        with open(self.file_path, "w") as file:
            json.dump(movies, file)
        return flag

    def update_movie(self, name):
        with open(self.file_path, "r") as file:
            movies = json.loads(file.read())
        answer = ''
        for movie in movies:
            if name.lower() == movie["name"].lower():
                note = input("Enter movie notes: ")
                movie["note"] = note
                answer = f"Movie {name} successfully updated"
                break
            else:
                answer = Fore.RED + f"Movie {name} doesn't exist!"
        print(answer)
        with open(self.file_path, "w") as file:
            json.dump(movies, file)
