class User(object):
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.id = 0


class UserList(object):
    def __init__(self):
        self.user_list = []

    def save_to_file(self):
        pass
        # TODO: Zapis do pliku

    def load_from_file(self):
        pass
        # TODO: Wczytywanie z pliku


if __name__ == "__main__":
    exit(10)
