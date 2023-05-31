from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import json
from colorama import Fore

def log_in(storage_lst):
    # Function to handle user login
    flag = "not found"
    while True:
        print("*** Log in ***")
        name_input = input(Fore.LIGHTWHITE_EX + "Enter username: ")
        password_input = input(Fore.LIGHTWHITE_EX + "Enter password: ")
        for account in storage_lst:
            dot_index = account["username"].index(".")
            if name_input.lower() == account["username"][:dot_index].lower() and password_input.lower() == account["password"].lower():
                if "csv" in account["username"]:
                    storage = StorageCsv(account["username"])
                    movie_app = MovieApp(storage)
                    if not movie_app.menu(len(movie_app._storage.list_movies())):
                        return  # Exit the login loop
                    flag = "found"
                elif "json" in account["username"]:
                    storage = StorageJson(account["username"])
                    movie_app = MovieApp(storage)
                    if not movie_app.menu(len(movie_app._storage.list_movies())):
                        return  # Exit the login loop
                    flag = "found"
                else:
                    flag = "not found"
        if flag == "not found":
            print(Fore.LIGHTWHITE_EX + "Login failed. Incorrect username or password. Please try again.")
            return
        else:
            return

def sign_up(storage_lst):
    # Function to handle user sign up
    flag = False
    print(Fore.LIGHTWHITE_EX + "--- Sign up ---")
    name_input = input(Fore.LIGHTWHITE_EX + "Enter username: ")
    password_input = input(Fore.LIGHTWHITE_EX + "Enter password: ")
    for account in storage_lst:
        dot_index = account["username"].index(".")
        if name_input.lower() == account["username"][:dot_index].lower():
            flag = True
    if not flag:
        print(Fore.LIGHTWHITE_EX + "1. json")
        print(Fore.LIGHTWHITE_EX + "2. csv")
        user_input = input(Fore.LIGHTWHITE_EX + "What file type would you like to save your movies in : ")
        if user_input == "1":
            accounts_dict = {'username': name_input + '.json', 'password': password_input}
            storage_lst.append(accounts_dict)
            with open("accounts.json", "w") as file:
                json.dump(storage_lst, file)
            with open(f"{name_input}.json", "w") as file:
                file.write("[]")
        if user_input == "2":
            accounts_dict = {'username': name_input + '.csv', 'password': password_input}
            storage_lst.append(accounts_dict)
            with open("accounts.json", "w") as file:
                json.dump(storage_lst, file)
            with open(f"{name_input}.csv", "w") as file:
                file.write("title,rating,year")
        print(Fore.LIGHTWHITE_EX + "You have successfully registered!")
        return
    else:
        print(Fore.LIGHTWHITE_EX + "Username already exists!")
        return

def main():
    with open('accounts.json', "r") as f:
        storage_lst = json.loads(f.read())

    while True:
        print(Fore.LIGHTWHITE_EX + "--- Welcome to the movie app ---")
        print(Fore.LIGHTWHITE_EX + "1. Log in.")
        print(Fore.LIGHTWHITE_EX + "2. Sign up")
        print(Fore.LIGHTWHITE_EX + "0. Quit.")
        user_input = input(Fore.LIGHTWHITE_EX + "Please enter your choice: ")

        if user_input == "1":
            log_in(storage_lst)
        elif user_input == "0":
            print("Bye!")
            return
        elif user_input == "2":
            sign_up(storage_lst)
        else:
            print(Fore.LIGHTWHITE_EX + "Please enter a number between 0 - 2!")

if __name__ == "__main__":
    main()
