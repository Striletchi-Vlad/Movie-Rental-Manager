import datetime
import unittest
from src.domain.client import Client
from src.domain.rental import Rental
from src.repository.client_repo import ClientRepo
from src.repository.movie_repo import MovieRepo
from src.repository.rental_repo import RentalRepo
from src.repository.undo_redo_repo import UndoRedoRepo
from src.services.movie_service import MovieService
from src.services.client_service import ClientService
from src.services.rental_service import RentalService, RentalServiceException
from src.domain.movie import *


class TestMovie(unittest.TestCase):
    def setUp(self) -> None:
        self.movie_id = "13"
        self.title = "aa"
        self.description = "bb"
        self.genre = "cc"
        self.my_movie = Movie(self.movie_id, self.title, self.description, self.genre)

    def testCorrectInit(self):
        self.assertEqual(self.my_movie.id, self.movie_id)
        self.assertEqual(self.my_movie.title, self.title)
        self.assertEqual(self.my_movie.description, self.description)
        self.assertEqual(self.my_movie.genre, self.genre)

    def testCorrectAssignment(self):
        title = "new"
        self.my_movie.title = title
        self.assertEqual(self.my_movie.title, title)


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        self.client_id = "13"
        name = "a"
        self.my_client = Client(self.client_id, name)

    def testCorrectInit(self):
        self.assertEqual(self.my_client.id, self.client_id)

    def testCorrectAssignment(self):
        name = "new"
        self.my_client.name = name
        self.assertEqual(self.my_client.name, name)


class TestMovieService(unittest.TestCase):
    def setUp(self) -> None:
        movie_id = "13"
        self.title = "aa"
        self.description = "bb"
        self.genre = "cc"
        self.my_movie = Movie(movie_id, self.title, self.description, self.genre)
        self.my_repo = MovieRepo()
        self.my_undo_redo_repo = UndoRedoRepo()
        self.my_rental_repo = RentalRepo()
        self.my_client_repo = ClientRepo()
        self.my_rental_service = RentalService(self.my_rental_repo, self.my_client_repo, self.my_repo,
                                               self.my_undo_redo_repo)
        self.my_service = MovieService(self.my_repo, self.my_undo_redo_repo, self.my_rental_service)
        self.my_service.add(self.title, self.description, self.genre)

    def testGetById(self):
        self.assertEqual(self.my_service.get_by_id(1), None)
        movie1 = self.my_service.get_by_id(0)
        self.assertNotEqual(self.my_movie.id, movie1.id)
        self.assertEqual(self.my_movie.title, movie1.title)
        self.assertEqual(self.my_movie.description, movie1.description)
        self.assertEqual(self.my_movie.genre, movie1.genre)

    def testRemove(self):
        self.my_service.remove(0)
        self.assertEqual(self.my_service.get_by_id(0), None)

    def testUpdate(self):
        title = "AA"
        self.my_service.update_by_id(0, title, self.description, self.genre)
        self.assertEqual(self.my_service.get_by_id(0).title, title)

    def testGetListWithKeyword(self):
        self.my_service.add("title1", "desc1", "genre1")
        self.my_service.add("title2", "desc2tle1", "genre2")

        searched_list = self.my_service.get_list_with_keyword("title1")
        self.assertEqual(searched_list, [Movie(1, "title1", "desc1", "genre1")])

        list_of_all = self.my_service.get_all()
        searched_list2 = self.my_service.get_list_with_keyword("tle1")
        self.assertEqual(searched_list2, [Movie(1, "title1", "desc1", "genre1"), Movie(2, "title2", "desc2tle1", "genre2")])


class TestClientService(unittest.TestCase):
    def setUp(self) -> None:
        client_id = "13"
        self.name = "a"
        self.my_client = Client(client_id, self.name)
        self.my_client_repo = ClientRepo()
        self.my_undo_redo_repo = UndoRedoRepo()
        self.my_rental_repo = RentalRepo()
        self.my_movie_repo = MovieRepo()
        self.my_rental_service = RentalService(self.my_rental_repo, self.my_client_repo, self.my_movie_repo,
                                               self.my_undo_redo_repo)
        self.my_service = ClientService(self.my_client_repo, self.my_undo_redo_repo, self.my_rental_service)
        self.my_service.add(self.name)

    def testGetById(self):
        client1 = self.my_service.get_by_id(0)
        self.assertNotEqual(self.my_client.id, client1.id)
        self.assertEqual(self.my_client.name, client1.name)

    def testRemove(self):
        self.my_service.remove(0)
        self.assertEqual(self.my_service.get_by_id(0), None)

    def testUpdate(self):
        name = "AA"
        self.my_service.update_by_id(0, name)
        self.assertEqual(self.my_service.get_by_id(0).name, name)

    def testGetListWithKeyword(self):
        self.my_service.add("client1AA")
        self.my_service.add("client2")
        searched_list = self.my_service.get_list_with_keyword("client1")
        self.assertEqual(searched_list, [Client(1, "client1AA")])

        searched_list = self.my_service.get_list_with_keyword("a")

        print([Client("13", "a"), Client(1, "client1")])
        list_to_compare_to = [Client(0, "a"), Client(1, "client1AA")]
        self.assertEqual(searched_list, list_to_compare_to)


class TestRentalService(unittest.TestCase):
    def setUp(self) -> None:
        self.rental_id = 13
        self.client_id = 14
        self.movie_id = 15
        self.my_rental_repo = RentalRepo()
        self.my_client_repo = ClientRepo()
        self.my_movie_repo = MovieRepo()
        self.my_undo_redo_repo = UndoRedoRepo()
        self.my_service = RentalService(self.my_rental_repo, self.my_client_repo, self.my_movie_repo, self.my_undo_redo_repo)
        self.my_rental = Rental(self.rental_id, self.movie_id, self.client_id, datetime.datetime.now(), datetime.datetime.now())
        self.my_service.add(self.movie_id, self.client_id, datetime.datetime.now(), datetime.datetime.now())

    def testValidateIdReturn(self):  
        with self.assertRaises(RentalServiceException) as re:
            self.my_service.validate_id_return(1, 15)
            self.assertEqual(str(re), "Id does not exist!")

        with self.assertRaises(RentalServiceException) as re:
            self.my_service.validate_id_return(0, 15)
            self.assertEqual(str(re), "That rental id does not belong to this client!")
        
        self.my_service.validate_id_return(0, 14)

    def testDeleteByClientId(self):
        rental1 = Rental(14, 15, 20, datetime.datetime.now(), datetime.datetime.now())
        rental2 = Rental(15, 15, 20, datetime.datetime.now(), datetime.datetime.now())

        self.my_rental_repo.add(rental1)
        self.my_rental_repo.add(rental2)
        self.my_service.delete_by_client_id(14)

        list_after_delete = self.my_service.get_all()
        self.assertEqual(list_after_delete, [rental1, rental2])

    def testDeleteByMovieId(self):
        rental1 = Rental(14, 15, 20, datetime.datetime.now(), datetime.datetime.now())
        rental2 = Rental(15, 16, 20, datetime.datetime.now(), datetime.datetime.now())

        self.my_rental_repo.add(rental1)
        self.my_rental_repo.add(rental2)
        self.my_service.delete_by_movie_id(15)

        list_after_delete = self.my_service.get_all()
        self.assertEqual(list_after_delete, [rental2])

    def testMostRentedMovies(self):
        rental1 = Rental(18, 15, 20, datetime.datetime.now(), datetime.datetime.now())
        rental2 = Rental(15, 16, 20, datetime.datetime.now(), datetime.datetime.now())
        rental3 = Rental(15, 16, 20, datetime.datetime.now(), datetime.datetime.now())
        rental4 = Rental(18, 16, 20, datetime.datetime.now(), datetime.datetime.now())
        rental5 = Rental(15, 14, 20, datetime.datetime.now(), datetime.datetime.now())

        self.my_rental_repo.add(rental1)
        self.my_rental_repo.add(rental2)
        self.my_rental_repo.add(rental3)
        self.my_rental_repo.add(rental4)
        self.my_rental_repo.add(rental5)
        list1 = self.my_service.most_rented_movies()

        self.assertEqual(list1, [16, 15, 14])

    def testMostActiveClients(self):
        rental1 = Rental(18, 15, 20, datetime.datetime.now(), datetime.datetime.now())
        rental2 = Rental(15, 16, 20, datetime.datetime.now(), datetime.datetime.now())
        rental3 = Rental(15, 16, 20, datetime.datetime.now(), datetime.datetime.now())
        rental4 = Rental(18, 16, 17, datetime.datetime.now(), datetime.datetime.now())
        rental5 = Rental(15, 14, 20, datetime.datetime.now(), datetime.datetime.now())

        self.my_rental_repo.add(rental1)
        self.my_rental_repo.add(rental2)
        self.my_rental_repo.add(rental3)
        self.my_rental_repo.add(rental4)
        self.my_rental_repo.add(rental5)
        list1 = self.my_service.most_active_clients()

        self.assertEqual(list1, [20, 14, 17])
