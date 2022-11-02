class ClientException(Exception):
    pass

class ClientRepo:

    def __init__(self) -> None:
        self.__list_of_clients = list()

    def add(self, client):
        self.__list_of_clients.append(client)
    
    def remove(self, id_to_remove):
        """
        Removes 1 single client based on id.
        """
        for item in self.__list_of_clients:
            if item.id == id_to_remove:
                self.__list_of_clients.remove(item)
                return

        raise ClientException("Id does not exist!")

    def get_by_id(self, id):

        for item in self.__list_of_clients:
            if item.id == id:
                return item

    def get_all(self):
        return self.__list_of_clients
