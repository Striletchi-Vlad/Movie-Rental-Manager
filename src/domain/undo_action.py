from src.domain.movie import Movie
from src.repository.movie_repo import MovieRepo
from src.services.movie_service import MovieService


class AbstractUndoAction:

    def execute(self):
        pass

    def execute_redo(self):
        pass


class UndoAction(AbstractUndoAction):

    def __init__(self, action_code, reverse_action_code, param, reverse_param, repo):
        self.__action_code = action_code
        self.__reverse_action_code = reverse_action_code
        self.__param = param
        self.__reverse_param = reverse_param
        self.__repo = repo

    def execute(self):
        self.__action_code(self.__repo, self.__param)

    def execute_redo(self):
        self.__reverse_action_code(self.__repo, self.__reverse_param)



class ComplexUndoAction(AbstractUndoAction):

    def __init__(self):
        self.__list_of_actions = list()

    def add_action_to_list(self, action):
        self.__list_of_actions.append(action)

    def execute(self):
        for i in reversed(range(len(self.__list_of_actions))):
            self.__list_of_actions[i].execute()

    def execute__redo(self):
        for i in reversed(range(len(self.__list_of_actions))):
            self.__list_of_actions[i].execute_redo()


class UndoRedoRepoException(Exception):
    pass


class UndoRedoRepo:

    def __init__(self):
        self.__list_of_actions = list()
        self.__index = 0

    def add_action_to_list(self, action):
        self.__list_of_actions = self.__list_of_actions[:self.__index]
        self.__list_of_actions.append(action)
        self.__index += 1

    def undo(self):
        if self.__index == 0:
            raise UndoRedoRepoException("No more undo!")
        self.__index -= 1
        self.__list_of_actions[self.__index].execute()

    def redo(self):
        if self.__index == len(self.__list_of_actions) - 1:
            raise UndoRedoRepoException("No more redo!")
        self.__index += 1
        self.__list_of_actions[self.__index].execute_redo()


movie_id = "13"
title = "aa"
description = "bb"
genre = "cc"
my_movie = Movie(movie_id, title, description, genre)
repo = MovieRepo()
repo.add(my_movie)

"""
my_undo_action = UndoAction(MovieRepo.remove, movie_id, repo)
my_undo_action.execute()

assert (len(repo.get_all()) == 0)

repo.remove(movie_id)
my_undo_action = UndoAction(MovieRepo.add, my_movie, repo)
my_undo_action.execute()

assert (len(repo.get_all()) == 1)


my_new_movie = Movie(movie_id, "new_title", description, genre)
repo.update(my_new_movie)
my_undo_action = UndoAction(MovieRepo.update, my_movie, repo)
my_undo_action.execute()

movie_from_repo = repo.get_by_id(movie_id)
assert(movie_from_repo.title == title)



my_service = MovieService(repo)
my_service.generate_10_values()

my_undo_action = ComplexUndoAction()
movies = my_service.get_all()
for movie in movies:
    if movie.genre != "Crime":
        undo_action = UndoAction(MovieRepo.add, movie, repo)
        my_undo_action.add_action_to_list(undo_action)


my_service.filter_by_genre("Crime")


assert (len(repo.get_all()) == 3)

my_undo_action.execute()

movies = my_service.get_all()
for movie in movies:
    print(movie)


assert (len(repo.get_all()) == 11)
"""
