class RepoException(Exception):
    pass


class MovieRepo:
    def __init__(self) -> None:
        self.__list_of_movies = list()
    
    def add(self, movie):
        self.__list_of_movies.append(movie)
    
    def remove(self, id_to_remove):
        """
        Removes 1 single movie based on id.
        """
        for item in self.__list_of_movies:
            if item.id == id_to_remove:
                self.__list_of_movies.remove(item)
                return

        raise RepoException("Id does not exist!")

    def get_by_id(self, id):
        for item in self.__list_of_movies:
            if item.id == id:
                return item
        return None

    def get_all(self):
        return self.__list_of_movies[:]

    def update(self, movie):
        for i in range(len(self.__list_of_movies)):
            if self.__list_of_movies[i].id == movie.id:
                self.__list_of_movies[i] = movie
                return

        raise RepoException("Id does not exist!")
