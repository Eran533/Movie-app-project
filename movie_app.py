import argparse
from storage_json import StorageJson
from matplotlib import pyplot as plt
import random
from fuzzywuzzy import process, fuzz
from colorama import Fore
from requests.exceptions import ConnectionError
from storage_csv import StorageCsv
import sys

class MovieApp:

    def __init__(self, storage):
        self._storage = storage

    def menu(self, movies_total):
        while True:
            print(Fore.CYAN + """
    ********** My Movies Database **********

    Menu:

    0. Exit
    1. List movies
    2. Add movie
    3. Delete movie
    4. Update movie
    5. Stats
    6. Random movie
    7. Search movie
    8. Movies sorted by rating
    9. Rating Histogram
    10. Generate website
            """)
            user_input = input("Enter choice (0-10): ")
            # Call the appropriate function based on user input
            if user_input == "1":
                self.list_movies(movies_total)
            elif user_input == "2":
                self.add_movie(movies_total)
            elif user_input == "3":
                self.delete_movie(movies_total)
            elif user_input == "4":
                self.update_movie(movies_total)
            elif user_input == "5":
                self.stats(movies_total)
            elif user_input == "6":
                self.get_random(movies_total)
            elif user_input == "7":
                self.search_movie(movies_total)
            elif user_input == "8":
                self.sort_by_rating(movies_total)
            elif user_input == "9":
                self.histogram(movies_total)
            elif user_input == "10":
                self.generate_website(movies_total)
            elif user_input == "0":
                return False
            else:
                self.menu(movies_total)
            return True

    def list_movies(self, movies_total):
        movies = self._storage.list_movies()
        print(f"""
        ********** {movies_total} movies in total **********
                        """)
        for movie in movies:
            print(f"Title: {movie['name']}, Rating: {movie['rating']}, Year of release: {movie['year']}, Poster Image URL: {movie['Poster']}")
        self.back_to_menu(movies_total)

    def add_movie(self, movies_total):
        flag = False
        name = input("Enter new movie name: ")
        movies = self._storage.list_movies()
        for movie in movies:
            if name.lower() != movie["name"].lower():
                flag = False
            else:
                flag = True
                break
        if not flag:
            try:
                added = self._storage.add_movie(name)
                if added:
                    movies_total += 1
            except (ConnectionError, KeyError) as e:
                print("There is an error! The internet connections do not work or the movie does not exist")
            self.back_to_menu(movies_total)
        else:
            print("This movie is already on the list")
            self.back_to_menu(movies_total)

    def delete_movie(self, movies_total):
        name = input("Enter movie name to delete: ")
        if self._storage.delete_movie(name):
            movies_total -= 1
        self.back_to_menu(movies_total)

    def update_movie(self, movies_total):
        name = input("Enter movie name: ")
        self._storage.update_movie(name)
        self.back_to_menu(movies_total)

    def stats(self, movies_total):
        movies = self._storage.list_movies()
        new_movies_dict = {}
        for movie in movies:
            new_movies_dict[movie["name"]] = float(movie["rating"])
        sort_movies = {key: val for key, val in sorted(new_movies_dict.items(), key=lambda val: val[1])}
        rating_lst = []
        for movie in movies:
            rating_lst.append(float(movie["rating"]))
        rating_lst.sort(reverse=True)
        average_rating = 0
        for rate in rating_lst:
            average_rating += rate
        average_rating = average_rating / movies_total
        if len(rating_lst) % 2 == 0:
            first_median = rating_lst[len(rating_lst) // 2]
            second_median = rating_lst[len(rating_lst) // 2 - 1]
            median = (first_median + second_median) / 2
        else:
            median = rating_lst[len(rating_lst) // 2]
        best_movie = max(sort_movies.values())
        best_movie_dict = dict((key, value) for key, value in sort_movies.items() if value == best_movie)
        worst_movie = min(sort_movies.values())
        worst_movie_dict = dict((key, value) for key, value in sort_movies.items() if value == worst_movie)
        print("""
    ********** Movies stats **********
        """)
        print(f"Average rating : {average_rating}")
        print(f"Median rating : {median}")
        print(f"The best movies : ")
        for k, v in best_movie_dict.items():
            print(f"{k} : {v}")
        print(f"The worst movies : ")
        for k, v in worst_movie_dict.items():
            print(f"{k} : {v}")
        self.back_to_menu(movies_total)

    def get_random(self, movies_total):
        movies = self._storage.list_movies()
        random_movie = random.choice(movies)
        print(
            f"Your movie for tonight: {random_movie['name']}, it's rated {random_movie['rating']}, Year of release: {random_movie['year']}")
        self.back_to_menu(movies_total)

    def search_movie(self, movies_total):
        movies = self._storage.list_movies()
        movie_names = []
        for movie in movies:
            movie_names.append(movie["name"])
        movie_name = input("Enter part of movie name: ")
        count = 0
        for movie in movies:
            if movie_name.upper() in movie["name"].upper():
                print(f"{movie['name']}, it's rated {movie['rating']}, Year of release: {movie['year']}")
                count += 1
        if count == 0:
            print(Fore.RED + f"The movie {movie_name} does not exist!")
            best_match = process.extract(movie_name, movie_names, scorer=fuzz.token_sort_ratio)
            for match in best_match:
                if match[1] > 50:
                    print("Did you mean : ")
                    print(f"{match[0]}")
        self.back_to_menu(movies_total)

    def sort_by_rating(self, movies_total):
        movies = self._storage.list_movies()
        new_movies_dict = {}
        for movie in movies:
            new_movies_dict[movie["name"]] = movie["rating"]
        sort_movies = {key: val for key, val in sorted(new_movies_dict.items(), key=lambda val: val[1])}
        for k, v in sort_movies.items():
            print(f"{k} : {v}")
        self.back_to_menu(movies_total)

    def back_to_menu(self, movies_total):
        user_input = input("""
Press enter to continue""")
        if user_input == "":
            self.menu(movies_total)
        else:
            self.back_to_menu(movies_total)

    def histogram(self, movies_total):
        movies = self._storage.list_movies()
        movie_rating = []
        for movie in movies:
            movie_rating.append(movie["rating"])
        movie_rating.sort(reverse=True)
        bins = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        plt.title("Ratings of the movies")
        plt.xlabel("Ratings")
        plt.ylabel("Frequency")
        plt.hist(movie_rating, bins=bins, edgecolor='black')
        save_histogram = input("Please enter a name for the file you want to save : ")
        plt.savefig(save_histogram, dpi=150)
        plt.show()
        print(f"{save_histogram} Saved successfully")
        self.back_to_menu(movies_total)

    def open_html_file(self):
        with open('index_template.html', 'r') as f:
            html_file = f.read()
            return html_file

    def update_website(self, movie):
        countries = []
        output = ""
        output += '<li>'
        output += '<div class="movie">'
        if "note" in movie:
            output += '<div class="container">'
            output += f'<a href="https://www.imdb.com/title/{movie["imdb_id"]}">'
            output += f'<img src={movie["Poster"]} alt="Avatar" class="image">'
            output += '<div class="overlay">'
            output += f'<div class="text">{movie["note"]}</div>'
            output += "</div>"
            output += '</a>'
            output += "</div>"
        else:
            output += f'<a href="https://www.imdb.com/title/{movie["imdb_id"]}">'
            output += '<img class="movie-poster"'
            output += f" src={movie['Poster']}/>"
            output += '</a>'
        output += f'<div class="movie-title">{movie["name"]}</div>'
        output += f'<div class="movie-year">{movie["year"]}</div>'
        output += f'<div class="rating">Rating : </div>'
        output += f'<div class="movie-rating">{movie["rating"]}</div>'
        if "," in movie["Country"]:
            for country in movie["Country"].split(", "):
                countries.append(country)
            for country in countries:
                country_image = self._storage.country_flag(country)
                output += f'<img class="country_flag"'
                output += f' src={country_image}>'
        else:
            country_image = self._storage.country_flag(movie["Country"])
            output += f'<img class="country_flag"'
            output += f' src={country_image}>'
        output += "</div>"
        output += "</li>"
        return output

    def generate_website(self, movies_total):
        original_html_file = self.open_html_file()
        output = ''
        movies = self._storage.list_movies()
        for movie in movies:
            output += self.update_website(movie)
        html_str = original_html_file.replace("__TEMPLATE_MOVIE_GRID__", output)
        with open('movie_website.html', 'w') as f:
            f.write(html_str)
        print("Successfully generated the website.")
        self.back_to_menu(movies_total)

    def run(self):
        movies = self._storage.list_movies()
        movies_total = len(movies)
        self.menu(movies_total)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My Movie Database')
    parser.add_argument('storage_file', type=str, help='Path to the storage file')
    args = parser.parse_args()
    storage_file = args.storage_file

    if storage_file.endswith('.json'):
        storage = StorageJson(storage_file)
    elif storage_file.endswith('.csv'):
        storage = StorageCsv(storage_file)
    else:
        print("Unsupported storage file format.")
        sys.exit()

    app = MovieApp(storage)
    app.run()
