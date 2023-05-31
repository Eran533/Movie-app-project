from storage_json import StorageJson
from storage_csv import StorageCsv

def test_storage_json():
    storage = StorageJson("eran.json")

    movies = storage.list_movies()
    assert isinstance(movies, list)

    added = storage.add_movie("Inception")
    assert added

    deleted = storage.delete_movie("Inception")
    assert deleted

    country_flag = storage.country_flag("United States")
    assert isinstance(country_flag, str)
    print("All tests passed successfully.")

def test_storage_csv():
    storage = StorageCsv("movies.csv")

    movies = storage.list_movies()
    assert isinstance(movies, list)

    added = storage.add_movie("Inception")
    assert added

    deleted = storage.delete_movie("Inception")
    assert deleted

    country_flag = storage.country_flag("United States")
    assert isinstance(country_flag, str)

    print("All tests passed successfully.")

test_storage_csv()
test_storage_json()
