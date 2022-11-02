class Rental:

    def __init__(self, rental_id, movie_id, client_id, rented_date, due_date):
        self.__rental_id = rental_id
        self.__movie_id = movie_id
        self.__client_id = client_id
        self.__rented_date = rented_date
        self.__due_date = due_date
        self.__returned_date = None

    @property
    def rental_id(self):
        return self.__rental_id

    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def client_id(self):
        return self.__client_id

    @property
    def rented_date(self):
        return self.__rented_date

    @property
    def due_date(self):
        return self.__due_date

    @property
    def returned_date(self):
        return self.__returned_date

    @returned_date.setter
    def returned_date(self, new_date):
        self.__returned_date = new_date

    def __str__(self):
        res = ""
        res += "\nRental id: " + str(self.__rental_id)
        res += "\nClient id: " + str(self.__client_id)
        res += "\nMovie id: " + str(self.__movie_id)
        res += "\nRented date: " + str(self.__rented_date)
        res += "\nDue date: " + str(self.__due_date)
        res += "\nReturned date: " + str(self.__returned_date)
        return res

    def __repr__(self):
        return str(self) + "\n"

