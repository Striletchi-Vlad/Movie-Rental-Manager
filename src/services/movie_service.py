from copy import deepcopy
from random import shuffle


from src.domain.movie import Movie


class MovieServiceException(Exception):
    pass


class MovieService:

    def __init__(self, repo, undo_redo_repo, rental_service) -> None:
        self.__repo = repo
        self.__undo_redo_repo = undo_redo_repo
        self.__rental_service = rental_service
        self.__movie_counter = 0

    def inc_movie_counter(self):
        self.__movie_counter += 1

    def add(self, title, desc, genre):
        new_movie = Movie(self.__movie_counter, title, desc, genre)
        self.__repo.add(new_movie)
        self.inc_movie_counter()

    def remove(self, id):
        self.__repo.remove(id)
        self.__rental_service.delete_by_movie_id(id)

    def get_by_id(self, id):
        return self.__repo.get_by_id(id)

    def get_all(self):
        return self.__repo.get_all()

    def update_by_id(self, id, title, desc, genre):
        item_to_update = self.get_by_id(id)
        item_to_update.title = title
        item_to_update.description = desc
        item_to_update.genre = genre

    def validate_id(self, id_to_val):
        if self.get_by_id(id_to_val) is None:
            raise MovieServiceException("Id does not exist!")

    def filter_by_genre(self, genre):
        movies = self.__repo.get_all()
        for movie in movies:
            if movie.genre != genre:
                self.__repo.remove(movie.id)

    def get_list_with_keyword(self, keyword):
        """
        !!!!!! CANNOT BE DONE WITH "FOR", IT SKIPS ELEMENTS WHEN DELETING
        :param keyword: already "casefold"-ed keyword
        :return: list of clients that have keyword in any of their fields
        """
        new_list = deepcopy(self.__repo.get_all())
        i = 0
        while i < len(new_list):
            if keyword not in str(new_list[i].id).casefold():
                if keyword not in new_list[i].title.casefold():
                    if keyword not in new_list[i].description.casefold():
                        if keyword not in new_list[i].genre.casefold():
                            new_list.remove(new_list[i])
                        else:
                            i += 1
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        return new_list

    def generate_10_values(self):
        m1 = {"title": "The Shawshank Redemption",
              "desc": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
              "genre": "Drama"}
        m2 = {"title": "The Godfather",
              "desc": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.",
              "genre": "Crime"}
        m3 = {"title": "The Dark Knight",
              "desc": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
              "genre": "Action"}
        m4 = {"title": "12 Angry Men",
              "desc": "The jury in a New York City murder trial is frustrated by a single member whose skeptical caution forces them to more carefully consider the evidence before jumping to a hasty verdict.",
              "genre": "Crime"}
        m5 = {"title": "Schindler's List",
              "desc": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
              "genre": "Biography"}
        m6 = {"title": "The Lord of the Rings: The Return of the King",
              "desc": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
              "genre": "Adventure"}
        m7 = {"title": "Pulp Fiction",
              "desc": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
              "genre": "Crime"}
        m8 = {"title": "The Good, the Bad and the Ugly",
              "desc": "A bounty hunting scam joins two men in an uneasy alliance against a third in a race to find a fortune in gold buried in a remote cemetery.",
              "genre": "Western"}
        m9 = {"title": "Fight Club",
              "desc": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
              "genre": "Drama"}
        m10 = {"title": "Forrest Gump",
              "desc": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.",
              "genre": "Romance"}

        movie_list = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]
        shuffle(movie_list)
        for item in movie_list:
            self.add(item["title"], item["desc"], item["genre"])

