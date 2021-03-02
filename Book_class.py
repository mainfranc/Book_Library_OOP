
class Book:
    """
    Book object class for storage in interface full_lib
    """
    def __init__(self, id: int, name: str, auth: str, year: int, desc: str):
        self._bookID = id
        self._book_name = name
        self._book_auth = auth
        self._book_year = year
        self._book_desc = desc

    @property
    def bookID(self):
        return self._bookID

    @bookID.setter
    def bookID(self, value: int):
        self._bookID = value

    @property
    def book_name(self):
        return self._book_name

    @book_name.setter
    def book_name(self, value: str):
        self._book_name = value

    @property
    def book_auth(self):
        return self._book_auth

    @book_auth.setter
    def book_auth(self, value: str):
        self._book_auth = value

    @property
    def book_year(self):
        return self._book_year

    @book_year.setter
    def book_year(self, value: int):
        if isinstance(value, (int, float)) and len(str(value)) == 4:
            self._book_year = value
        else:
            raise ValueError('Please enter the correct year')

    @property
    def book_desc(self):
        return self._book_desc

    @book_desc.setter
    def book_desc(self, value: str):
        self._book_desc = value
