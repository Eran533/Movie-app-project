from istorage import IStorage
import requests

class StorageCsv(IStorage):

    def __init__(self, file_path):
        self.file_path = file_path

    def api(self, movie_name):
        api_key = "26e330a6&t"
        name_movie = movie_name
        url = f"https://www.omdbapi.com/?apikey={api_key}&t={name_movie}"
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
            first_line = file.readline()
            read = file.read()
        movies = []
        for line in read.split("\n"):
            if len(line.split(",")) > 3:
                movie_dict = self.api(line.split(",")[0])
                name = movie_dict['Title']
                year = movie_dict['Year']
                rating = movie_dict['imdbRating']
                postr = movie_dict['Poster']
                imdb_id = movie_dict['imdbID']
                country = movie_dict['Country']
                movie_dict = {'name': name, 'rating': rating, 'year': year, 'Poster': postr, 'imdb_id': imdb_id,
                              'Country': country, "note": line.split(",")[-1]}
                movies.append(movie_dict)
            elif len(line.split(",")) > 1:
                movie_dict = self.api(line.split(",")[0])
                name = movie_dict['Title']
                year = movie_dict['Year']
                rating = movie_dict['imdbRating']
                postr = movie_dict['Poster']
                imdb_id = movie_dict['imdbID']
                country = movie_dict['Country']
                movie_dict = {'name': name, 'rating': rating, 'year': year, 'Poster': postr, 'imdb_id': imdb_id, 'Country': country}
                movies.append(movie_dict)
            else:
                continue
        return movies

    def add_movie(self, name):
        movie_json = self.api(name)
        if movie_json.get('Error'):
            print(f"Movie {name} not found!")
            return False
        name = movie_json['Title']
        year = movie_json['Year']
        rating = movie_json['imdbRating']
        with open(self.file_path, "a") as file:
            file.write(f"\n{name},{rating},{year}")
        print(f"Movie {name} was successfully added")
        return True

    def delete_movie(self, name):
        deleted_movie = ''
        flag = False
        with open(self.file_path, "r") as file:
            movies = file.readlines()
        with open(self.file_path, "w") as file:
            for movie in movies:
                if name.lower() != movie.split(",")[0].lower():
                    file.write(movie)
                else:
                    flag = True
                    deleted_movie = movie.split(",")[0]
        if flag:
            print(f"Movie {deleted_movie} successfully deleted")
            return True
        else:
            print(f"Movie {name} not found!")
            return False

    def update_movie(self, name):
        movie_found = False
        answer = ""
        with open(self.file_path, "r") as file:
            movies = file.readlines()
        with open(self.file_path, "w") as file:
            for movie in movies:
                if name.lower() != movie.split(",")[0].lower():
                    file.write(movie)
                else:
                    movie_found = True
                    note = input("Enter movie notes: ")
                    if movie.count(",") > 2:
                        update_movie = movie.replace(movie.split(",")[-1], (note + "\n"))
                        answer = f"Movie {name} successfully updated"
                        file.write(update_movie)
                    else:
                        update_movie = movie.strip() + "," + note + "\n"
                        answer = f"Movie {name} successfully updated"
                        file.write(update_movie)

        if not movie_found:
            answer = f"Movie {name} doesn't exist!"

        print(answer)
