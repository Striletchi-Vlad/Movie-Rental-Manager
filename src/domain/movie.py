import textwrap


class Movie:

    def __init__(self, id, title, description, genre) -> None:
        self.__movie_id = id
        self.__title = title
        self.__description = description
        self.__genre = genre

    @property
    def id(self):
        return self.__movie_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, desc):
        self.__description = desc
    
    @property 
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    def __str__(self) -> str:
        res = ""
        res += ("Id: " + str(self.id))
        res += ("\nTitle: " + str(self.title))
        res += "\nDescription: "
        temp_desc = textwrap.wrap(self.description)
        for item in temp_desc:
            res += ("\n" + item)
        res += ("\nGenre: " + str(self.genre) + "\n\n")
        return res

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        if self.__movie_id == other.id:
            if self.__title == other.title:
                if self.__description == other.description:
                    if self.__genre == other.genre:
                        return True
        return False
