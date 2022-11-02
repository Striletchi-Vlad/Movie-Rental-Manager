class RepoException(Exception):
    pass


class RentalRepo:

    def __init__(self) -> None:
        self.__list_of_rentals = list()

    def add(self, rental):
        self.__list_of_rentals.append(rental)

    def remove(self, id_to_remove):
        """
        Removes 1 single movie based on id.
        """
        for item in self.__list_of_rentals:
            if item.id == id_to_remove:
                self.__list_of_rentals.remove(item)
                return

        raise RepoException("Id does not exist!")

    def get_by_id(self, id):
        for item in self.__list_of_rentals:
            if item.rental_id == id:
                return item
        return None

    def get_by_client_id(self, id):
        list_to_return = list()
        for item in self.__list_of_rentals:
            if item.client_id == id:
                list_to_return.append(item)
        return list_to_return

    def get_all(self):
        return self.__list_of_rentals
