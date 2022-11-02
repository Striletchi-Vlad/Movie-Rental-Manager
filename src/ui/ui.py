import datetime

from src.services.client_service import ClientService, ClientServiceException
from src.repository.movie_repo import RepoException
from src.services.movie_service import MovieService, MovieServiceException
from src.services.rental_service import RentalService, RentalServiceException
from src.ui.ui_misc import pretty_print_list


class UIException(Exception):
    pass


class Menu:

    def __init__(self, movieservice, clientservice, rentalservice) -> None:
        self.__movieservice = movieservice
        self.__clientservice = clientservice
        self.__rentalservice = rentalservice
        self.__option = ""

    def print_options(self):
        print("\t1. Add Movie")
        print("\t2. Remove Movie")
        print("\t3. Update Movie")
        print("\t4. List Movies")
        print("")
        print("\t5. Add Client")
        print("\t6. Remove Client")
        print("\t7. Update Client")
        print("\t8. List Clients")
        print("")
        print("\t9. Rent a movie")
        print("\t10. Return a movie")
        print("\t11. List rentals")
        print("")
        print("\t12. Search")
        print("\t13. Show most rented movies")
        print("\t14. Show most active clients")
        print("")
        print("\t15. Exit.")

    @property
    def opt(self):
        return self.__option

    def set_option(self, new_option):
        if new_option not in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']:
            raise UIException("option not available.")
        else:
            self.__option = new_option

    def read_option(self):
        x = input("Choose an option: ")
        x = x.strip()
        self.set_option(x)

    def execute_option(self):
        
        if self.__option == "1":
            self.opt1()
        if self.__option == "2":
            self.opt2()
        if self.__option == "3":
            self.opt3()
        if self.__option == "4":
            self.opt4()
        if self.__option == "5":
            self.opt5()
        if self.__option == "6":
            self.opt6()
        if self.__option == "7":
            self.opt7()
        if self.__option == "8":
            self.opt8()
        if self.__option == "9":
            self.opt9()
        if self.__option == "10":
            self.opt10()
        if self.__option == "11":
            self.opt11()
        if self.__option == "12":
            self.opt12()
        if self.__option == "13":
            self.opt13()
        if self.__option == "14":
            self.opt14()
        if self.__option == "15":
            exit()

    def opt1(self):
        new_title = input("Input title: ")
        new_desc = input("Input movie description: ")
        new_genre = input("Input genre: ")
        self.__movieservice.add(new_title, new_desc, new_genre)

    def opt2(self):
        id_to_remove = input("Id to remove: ")
        if not id_to_remove.isnumeric():
            raise UIException("Id must be numeric!")
        self.__movieservice.remove(int(id_to_remove))

    def opt3(self):
        id_to_update = input("Id to update: ")
        if not id_to_update.isnumeric():
            raise UIException("Id must be numeric!")
        new_title = input("Input title: ")
        new_desc = input("Input movie description: ")
        new_genre = input("Input genre: ")

        self.__movieservice.update_by_id(int(id_to_update), new_title, new_desc, new_genre)

    def opt4(self):
        pretty_print_list(self.__movieservice.get_all())

    def opt5(self):
        new_name = input("Input client name: ")
        self.__clientservice.add(new_name)

    def opt6(self):
        id_to_remove = input("Id to remove: ")
        if not id_to_remove.isnumeric():
            raise UIException("Id must be numeric!")
        self.__clientservice.remove(int(id_to_remove))

    def opt7(self):
        id_to_update = input("Id to update: ")
        if not id_to_update.isnumeric():
            raise UIException("Id must be numeric!")
        new_name = input("Input client name: ")

        self.__clientservice.update_by_id(int(id_to_update), new_name)

    def opt8(self):
        pretty_print_list(self.__clientservice.get_all())

    def opt9(self):
        self.check_movies_clients_nonempty()
        print("The list of clients is: ")
        pretty_print_list(self.__clientservice.get_all())  # self.opt8 WHY DOESNT THIS WORK?
        client_id = input("\tEnter your client ID: ")
        if not client_id.isnumeric():
            raise UIException("Id must be numeric!")
        self.__clientservice.validate_id(int(client_id))
        self.__rentalservice.validate_eligible_client(int(client_id))

        print("The list of available movies is: ")
        pretty_print_list(self.__movieservice.get_all())  # self.opt4
        movie_id = input("Which movie do you want to rent? (Movie ID): ")
        if not movie_id.isnumeric():
            raise UIException("Id must be numeric!")
        self.__movieservice.validate_id(int(movie_id))

        rented_date = datetime.datetime.now()
        due_date = rented_date + datetime.timedelta(seconds=30)
        # just a default value, movie is rented for 30 seconds to make it easy to showcase
        self.__rentalservice.validate_id_rent(int(client_id), int(movie_id))
        self.__rentalservice.add(int(movie_id), int(client_id), rented_date, due_date)

    def opt10(self):
        self.check_movies_clients_nonempty()
        print("The list of clients is: ")
        pretty_print_list(self.__clientservice.get_all())  # self.opt8
        client_id = input("\tEnter your client ID: ")
        if not client_id.isnumeric():
            raise UIException("Id must be numeric!")
        self.__clientservice.validate_id(int(client_id))

        print("The list of your rentals is: ")
        pretty_print_list(self.__rentalservice.get_by_client_id(int(client_id)))
        rental_id = input("Which movie do you want to return? (Enter the rental id): ")
        if not rental_id.isnumeric():
            raise UIException("Id must be numeric!")
        self.__rentalservice.validate_id_return(int(rental_id), int(client_id))
        self.__rentalservice.return_movie(int(rental_id))

    def opt11(self):
        pretty_print_list(self.__rentalservice.get_all())

    def opt12(self):
        keyword = input("Provide a keyword: ").casefold()
        search_res = self.__movieservice.get_list_with_keyword(keyword)
        if not search_res:
            print("No results found in movie database.")
        else:
            print("Results in movies: \n")
            pretty_print_list(self.__movieservice.get_list_with_keyword(keyword))

        search_res = self.__clientservice.get_list_with_keyword(keyword)
        if not search_res:
            print("No results found in client database.")
        else:
            print("Results in clients: \n")
            pretty_print_list(self.__clientservice.get_list_with_keyword(keyword))

    def opt13(self):
        l1 = self.__rentalservice.most_rented_movies()
        if l1:
            print("Most rented movies are: ")
            for item in l1:
                print(self.__movieservice.get_by_id(item))
        else:
            print("No movies rented thus far.")

    def opt14(self):
        l1 = self.__rentalservice.most_active_clients()
        if l1:
            print("Most active clients are: ")
            for item in l1:
                print(self.__clientservice.get_by_id(item))
        else:
            print("No clients have rented any movies thus far.")

    def check_movies_clients_nonempty(self):
        if not self.__clientservice.get_all():
            raise UIException("There are no clients!")
        if not self.__movieservice.get_all():
            raise UIException("There are no movies!")

    def start(self):
        self.__movieservice.generate_10_values()
        while True:
            try:
                self.print_options()
                self.read_option()
                self.execute_option()
            except UIException as ue:
                print(str(ue))
            except RepoException as re:
                print(str(re))
            except ClientServiceException as se:
                print(str(se))
            except MovieServiceException as se:
                print(str(se))
            except RentalServiceException as se:
                print(str(se))
