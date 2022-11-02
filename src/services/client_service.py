from copy import deepcopy

from src.repository.client_repo import ClientRepo
from src.domain.client import Client


class ClientServiceException(Exception):
    pass


class ClientService:

    def __init__(self, repo, undo_redo_repo, rental_service) -> None:
        self.__repo = repo
        self.__undo_redo_repo = undo_redo_repo
        self.__rental_service = rental_service
        self.__client_counter = 0

    def inc_client_counter(self):
        self.__client_counter += 1

    def add(self, name):
        new_client = Client(self.__client_counter, name)
        self.__repo.add(new_client)
        self.inc_client_counter()

    def remove(self, id):
        self.__repo.remove(id)
        self.__rental_service.delete_by_client_id(id)

    def get_by_id(self, id):
        return self.__repo.get_by_id(id)

    def get_all(self):
        return self.__repo.get_all()

    def update_by_id(self, id, name):
        item_to_update = self.get_by_id(id)
        item_to_update.name = name

    def validate_id(self, id_to_val):
        if self.get_by_id(id_to_val) is None:
            raise ClientServiceException("Id does not exist!")

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
                if keyword not in new_list[i].name.casefold():
                    new_list.remove(new_list[i])
                else:
                    i += 1
            else:
                i += 1
        return new_list
