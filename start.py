from src.domain.undo_action import UndoRedoRepo
from src.ui.ui import Menu
from src.repository.rental_repo import RentalRepo
from src.repository.movie_repo import MovieRepo
from src.repository.client_repo import ClientRepo
from src.services.rental_service import RentalService
from src.services.movie_service import MovieService
from src.services.client_service import ClientService

# TODO Service for undo_redo_repo
# TODO UI for the undo service

my_movie_repo = MovieRepo()
my_client_repo = ClientRepo()
my_rental_repo = RentalRepo()
my_undo_redo_repo = UndoRedoRepo()

my_rental_service = RentalService(my_rental_repo, my_client_repo, my_movie_repo, my_undo_redo_repo)
my_movie_service = MovieService(my_movie_repo, my_undo_redo_repo, my_rental_service)
my_client_service = ClientService(my_client_repo, my_undo_redo_repo, my_rental_service)


my_menu = Menu(my_movie_service, my_client_service, my_rental_service)
my_menu.start()
