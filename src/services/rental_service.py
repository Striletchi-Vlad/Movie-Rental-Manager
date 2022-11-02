from copy import deepcopy
from datetime import datetime
from src.domain.rental import Rental
from src.services.rental_service_misc import movie_key_function


class RentalServiceException(Exception):
    pass


class RentalService:

    def __init__(self, rental_repo, client_repo, movie_repo, undo_redo_repo) -> None:
        self.__rental_repo = rental_repo
        self.__client_repo = client_repo
        self.__movie_repo = movie_repo
        self.__undo_redo_repo = undo_redo_repo
        self.__rental_counter = 0

    def inc_rental_counter(self):
        self.__rental_counter += 1

    def add(self, movie_id, client_id, rented_date, due_date):
        new_rental = Rental(self.__rental_counter, movie_id, client_id, rented_date, due_date)
        self.__rental_repo.add(new_rental)
        self.inc_rental_counter()

    def return_movie(self, rental_id):
        rental_to_return = self.__rental_repo.get_by_id(rental_id)
        rental_to_return.returned_date = datetime.now()

    def delete_by_client_id(self, client_id):
        list1 = self.__rental_repo.get_all()
        i = 0
        while i < len(list1):
            if list1[i].client_id == client_id:
                list1.remove(list1[i])
            else:
                i += 1

    def delete_by_movie_id(self, movie_id):
        list1 = self.__rental_repo.get_all()
        i = 0
        while i < len(list1):
            if list1[i].movie_id == movie_id:
                list1.remove(list1[i])
            else:
                i += 1

    def get_by_id(self, id):
        return self.__rental_repo.get_by_id(id)

    def get_by_client_id(self, id):
        return self.__rental_repo.get_by_client_id(id)

    def get_all(self):
        return self.__rental_repo.get_all()

    def validate_id_rent(self, client_id, movie_id):
        for item in self.__rental_repo.get_all():
            if item.client_id == client_id:
                if item.movie_id == movie_id:
                    raise RentalServiceException("You cannot rent the same movie twice!")

    def validate_id_return(self, rental_id, client_id):
        if self.get_by_id(rental_id) is None:
            raise RentalServiceException("Id does not exist!")
        if self.get_by_id(rental_id) not in self.get_by_client_id(client_id):
            raise RentalServiceException("That rental id does not belong to this client!")

    def validate_eligible_client(self, client_id):
        list_of_rentals = self.__rental_repo.get_all()
        current_moment = datetime.now()
        for item in list_of_rentals:
            if item.client_id == client_id:
                if item.due_date < current_moment:
                    if item.returned_date is None:
                        raise RentalServiceException("You must first return the movies that have passed their due date!")

    def most_rented_movies(self):
        """
        :return: list of movies, descending, sorted "by occurrence vector"
        """
        list1 = self.__rental_repo.get_all()
        dict_of_movie_index = dict()
        for item in list1:
            if item.movie_id not in dict_of_movie_index:
                dict_of_movie_index[item.movie_id] = 0
            dict_of_movie_index[item.movie_id] += 1

        res = sorted(dict_of_movie_index, reverse=True, key=dict_of_movie_index.get)
        return res

    def most_active_clients(self):
        """
        :return: list of clients, descending, sorted "by occurrence vector"
        """
        list1 = self.__rental_repo.get_all()
        dict_of_client_index = dict()
        for item in list1:
            if item.client_id not in dict_of_client_index:
                dict_of_client_index[item.client_id] = 0
            dict_of_client_index[item.client_id] += 1

        res = sorted(dict_of_client_index, reverse=True, key=dict_of_client_index.get)
        return res
