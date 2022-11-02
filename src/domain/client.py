class Client:

    def __init__(self, id, name) -> None:
        self.__client_id = id
        self.__name = name

    @property
    def id(self):
        return self.__client_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __str__(self) -> str:
        res = ""
        res += ("Id: " + str(self.id))
        res += ("\nClient name: " + self.name + "\n")
        return res

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        if self.id == other.id:
            if self.__name == other.name:
                return True
        return False
