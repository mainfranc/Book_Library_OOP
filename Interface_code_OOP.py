import tkinter as tk
import sqlite3
from contextlib import closing


class Interface:
    def __init__(self):
        self.db_name = ''
        self.db_table_name = ''
        self.db_conn = None
        self.__full_lib = []
        self.root = None
        self.__book_name_text = None
        self.__book_author_text = None
        self.__book_year_text = None
        self.__book_desc_text = None
        self.conn_established = False

    # Interface Methods
    def main(self):
        """
        main procedure creting the first screen
        :return:
        """
        self.root = tk.Tk()
        self.root.title('Book library')
        if all([self.db_table_name, self.db_name]):
            self.add_button(self.root, 'Add Book', 20, 1, 1, 0, lambda: self.add_books())
            self.add_button(self.root, 'Search Books', 20, 1, 2, 0, lambda: self.search_books(self.__full_lib))
            self.__full_lib = self.import_func_db()
        self.add_label(self.root, "input path to the dataBase", 20, 1, 3, 0)
        db_path_text_box = self.add_textbox(self.root, self.db_name, 20, 2, 3, 1)
        self.add_label(self.root, "input table name", 20, 1, 4, 0)
        tbl_text_box = self.add_textbox(self.root, self.db_table_name, 20, 1, 4, 1)
        self.add_button(self.root, 'Set DataBase Source', 20, 1, 5, 0, lambda: self.set_db_source(
            db_path_text_box.get("1.0", 'end-1c'), tbl_text_box.get("1.0", 'end-1c')))
        self.root.mainloop()

    @staticmethod
    def add_label(area, txt: str, w: int, h: int, r: int, c: int):
        """
        adds the label into the selected frame
        :param area: area to insert
        :param txt: caption
        :param w: width
        :param h: height
        :param r: row in grid
        :param c: column in grid
        :return: label object
        """
        lbl = tk.Label(area, text=txt, width=w, height=h)
        lbl.grid(row=r, column=c, sticky='nsew')
        return lbl

    @staticmethod
    def add_textbox(area, txt: str, w: int, h: int, r: int, c: int):
        """
        adds the textbox into the selected frame
        :param area: area to insert
        :param txt: standard value
        :param w: width
        :param h: height
        :param r: row in grid
        :param c: column in grid
        :return: textbox object
        """
        tb = tk.Text(area, width=w, height=h)
        tb.grid(row=r, column=c, sticky='nsew')
        tb.insert('end-1c', txt)
        return tb

    @staticmethod
    def add_button(area, txt: str, w: int, h: int, r: int, c: int, func_):
        """
        add button inth the area
        :param area: area to insert
        :param txt: caption
        :param w: width
        :param h: height
        :param r: row in grid
        :param c: column in grid
        :param func_: command must be executed
        :return: button object
        """
        button = tk.Button(area, text=txt, width=w, height=h, font=('arial', 16, 'bold'), command=func_)
        button.grid(row=r, column=c, sticky='nsew')
        return button

    def set_db_source(self, path: str, table_name: str):
        """
        set the db connection
        :param path: path the the databse. if the database doesn't exists - the new db will be connected
        :param table_name: table name. if there are no such table in the db - the table with the proper columns will be created
        :return: None
        """
        self.db_name = path
        self.db_table_name = table_name
        self.db_conn = DBConnector(self)
        self.db_conn.connect_to_the_db()

    def back_to_main(self):
        """
        go back to the main screen
        :return: None
        """
        self.root.destroy()
        self.main()

    def create_header(self, root):
        """
        creates the header for the several screens
        :param root: area to insert the header
        :return: header
        """
        self.add_button(root, 'Back to main', 20, 1, 0, 0, lambda: self.back_to_main())
        self.add_label(root, "input book name", 20, 1, 1, 0)
        self.add_label(root, "input book author", 20, 1, 1, 1)
        self.add_label(root, "input book year", 20, 1, 1, 2)
        self.add_label(root, "input book description", 24, 1, 1, 3)
        self.__book_name_text = self.add_textbox(root, '', 20, 1, 2, 0)
        self.__book_author_text = self.add_textbox(root, '', 20, 1, 2, 1)
        self.__book_year_text = self.add_textbox(root, '', 20, 1, 2, 2)
        self.__book_desc_text = self.add_textbox(root, '', 24, 1, 2, 3)

    def clear_textboxes(self):
        """
        clear the textboxes in the header
        :return: None
        """
        self.__book_name_text.delete("1.0", 'end')
        self.__book_author_text.delete("1.0", 'end')
        self.__book_year_text.delete("1.0", 'end')
        self.__book_desc_text.delete("1.0", 'end')

    def add_books(self):
        """
        add books screen
        :return: None
        """
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title('Add book')
        self.create_header(self.root)
        self.add_button(self.root, 'Add book', 12, 1, 3, 0, lambda: self.lib_append())
        self.root.mainloop()

    def edit_screen(self, name_: str, auth_: str, year_: str, desc_: str):
        """
        screen for the edition of the record
        :param name_: new name value
        :param auth_: new author value
        :param year_: new year value
        :param desc_: new description value
        :return: None
        """
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title('enter the new values')
        self.create_header(self.root)
        self.__book_name_text.insert('end-1c', name_)
        self.__book_author_text.insert('end-1c', auth_)
        self.__book_year_text.insert('end-1c', year_)
        self.__book_desc_text.insert('end-1c', desc_)
        self.add_button(self.root, 'Edit entry', 12, 1, 3, 0, lambda: self.change_entry(name_, auth_,
                                                                                        year_, desc_))

    def search_books(self, show_lib: list):
        """
        search books screen with the full list of the library
        :param show_lib: lib to display
        :return: None
        """
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title('View books')
        main_frame = tk.Frame(self.root)
        main_frame.pack()
        self.create_header(main_frame)

        self.add_button(main_frame, 'sort by name', 12, 1, 3, 0,
                        lambda: self.search_books(sorted(show_lib,key= lambda book: book.book_name)))
        self.add_button(main_frame, 'sort by author', 12, 1, 3, 1,
                        lambda: self.search_books(sorted(show_lib, key=lambda book: book.book_auth)))
        self.add_button(main_frame, 'sort by year', 12, 1, 3, 2,
                        lambda: self.search_books(sorted(show_lib, key=lambda book: book.book_year)))
        self.add_button(main_frame, 'sort by description', 12, 1, 3, 3,
                        lambda: self.search_books(sorted(show_lib, key=lambda book: book.book_desc)))

        self.add_button(main_frame, 'Search book', 12, 1, 4, 0, lambda: self.lib_filter())
        self.add_button(main_frame, 'Clear search', 12, 1, 4, 1, lambda: self.search_books(self.__full_lib))
        table_frame = tk.Frame(self.root)
        canvas = tk.Canvas(table_frame)
        y_scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=y_scrollbar.set)
        for rw in range(len(show_lib)):
            addition_ = self.add_textbox(scrollable_frame, str(rw + 1), 3, 2, rw, 0)
            row_insertion = (show_lib[rw].book_name, show_lib[rw].book_auth,
                             show_lib[rw].book_year, show_lib[rw].book_desc)
            for cl in range(4):
                addition_ = self.add_textbox(scrollable_frame, row_insertion[cl], 24 if cl == 3 else 16, 2, rw, cl + 1)
            self.add_button(scrollable_frame, 'Edit', 3, 2, rw, 5,
                            lambda r=rw: self.edit_screen(show_lib[r].book_name,
                                                          show_lib[r].book_auth,
                                                          show_lib[r].book_year,
                                                          show_lib[r].book_desc))
            self.add_button(scrollable_frame, 'Remove', 6, 2, rw, 6,
                            lambda r=rw: self.remove_entry(show_lib[r].book_name,
                                                           show_lib[r].book_auth,
                                                           show_lib[r].book_year,
                                                           show_lib[r].book_desc))
        table_frame.pack(fill="both")
        canvas.pack(side="left", fill="both", expand=True)
        y_scrollbar.pack(side="right", fill="y")
        self.root.mainloop()

    class pop_up:
        """
        pop up messages
        """
        def __init__(self, inf_: str, obj_):
            """
            creation of the pop up
            :param inf_: text to display
            :param obj_: father object
            """
            self.pop_up_root = tk.Tk()
            self.pop_up_root.wm_title("!")
            label = tk.Label(self.pop_up_root, text=inf_, font=('arial', 12))
            label.pack(side="top", fill="x", pady=10)
            but_ = tk.Button(self.pop_up_root, text="Ok", command=lambda: self.destroy_addition(obj_, inf_))
            but_.pack()
            self.pop_up_root.mainloop()

        def destroy_addition(self, obj_, inf_):
            """
            Kill the pop-up object
            :param obj_: father object
            :param inf_: inf message
            :return: None
            """
            self.pop_up_root.destroy()
            if "database" in inf_: obj_.back_to_main()

    # Library Methods
    def lib_append(self):
        """
        append to library
        :return: None
        """
        nm = self.__book_name_text.get("1.0", 'end-1c')
        auth = self.__book_author_text.get("1.0", 'end-1c')
        yr = self.__book_year_text.get("1.0", 'end-1c')
        des = self.__book_desc_text.get("1.0", 'end-1c')
        if all([nm, auth]):
            if not yr.isnumeric():
                self.pop_up("Please enter the year as number", self)
            else:
                book_to_add = Book(0, nm, auth, yr, des)
                self.db_conn.append_to_db(nm, auth, yr, des)
                book_to_add.bookID = self.db_conn.read_db(nm, auth, yr, des)[0][0]
                self.__full_lib.append(book_to_add)
                self.__full_lib = sorted(self.__full_lib, key=lambda book: book.book_name)
                self.clear_textboxes()
        else:
            self.pop_up("Please fill book name and author fields", self)

    def lib_filter(self):
        """
        Filters library
        :return: None
        """
        self.__full_lib = sorted(self.__full_lib, key=lambda book: book.book_name)
        lib_to_show = []
        nm = self.__book_name_text.get("1.0", 'end-1c')
        auth = self.__book_author_text.get("1.0", 'end-1c')
        yr = self.__book_year_text.get("1.0", 'end-1c')
        desc = self.__book_desc_text.get("1.0", 'end-1c')
        for book_ in self.__full_lib:
            if all([nm in book_.book_name
                    and auth in book_.book_auth
                    and str(yr) in str(book_.book_year)
                    and desc in book_.book_desc]):
                lib_to_show.append(book_)
        self.search_books(lib_to_show)

    def change_entry(self, name_old: str, auth_old: str, year_old: str, desc_old: str):
        """
        change the entry
        :param name_old: old name to change
        :param auth_old: Old author to change
        :param year_old: old year to change
        :param desc_old: old description to change
        :return: None
        """
        self.__full_lib = sorted(self.__full_lib, key=lambda book: book.book_name)
        nm = self.__book_name_text.get("1.0", 'end-1c')
        auth = self.__book_author_text.get("1.0", 'end-1c')
        yr = self.__book_year_text.get("1.0", 'end-1c')
        des = self.__book_desc_text.get("1.0", 'end-1c')
        if all([self.__book_name_text, self.__book_author_text]):
            if not yr.isnumeric():
                self.pop_up("Please enter the year as number", self)
            else:
                str_to_search = f'{name_old};{auth_old};{year_old};{desc_old}'
                join_lst = self.joined_list(self.__full_lib)
                ind_ = self.binary_search(str_to_search, join_lst)
                book_id = self.__full_lib[ind_].bookID
                self.__full_lib[ind_] = Book(book_id, nm, auth, yr, des)
                self.db_conn.change_entry(nm, auth, yr, des, book_id)
                self.search_books(self.__full_lib)
        else:
            self.pop_up("Please fill book name and author fields", self)

    def remove_entry(self, name_: str, auth_: str, year_: str, desc_: str):
        """
        removes the record
        :param name_: name to search
        :param auth_: author to search
        :param year_: year to search
        :param desc_: description to search
        :return:
        """
        self.__full_lib = sorted(self.__full_lib, key=lambda book: book.book_name)
        str_to_search = f'{name_};{auth_};{year_};{desc_}'
        join_lst = self.joined_list(self.__full_lib)
        ind_ = self.binary_search(str_to_search, join_lst)
        book_id = self.__full_lib[ind_].bookID
        self.db_conn.remove_entry(book_id)
        self.__full_lib.pop(ind_)
        self.search_books(self.__full_lib)

    @staticmethod
    def joined_list(lst: list):
        """
        Creates the string from the list
        :param lst: list
        :return:
        """
        return [f"{i.book_name};{i.book_auth};{i.book_year};{i.book_desc}" for i in lst]

    @staticmethod
    def binary_search(elem: any, arr: list):
        """
        search the element in the array
        :param elem: element to search
        :param arr: list
        :return: index
        """
        if arr:

            len_of_curr_d = len(arr) // 2 + 1
            beg_d = 0
            while elem != arr[beg_d + len_of_curr_d - 1] and len_of_curr_d != 1:
                if elem > arr[beg_d + len_of_curr_d - 1]:
                    beg_d += len_of_curr_d
                if not len_of_curr_d % 2:
                    len_of_curr_d //= 2
                else:
                    len_of_curr_d = len_of_curr_d // 2 + 1
            if arr[beg_d] == elem:
                return beg_d
            if beg_d + len_of_curr_d < len(arr):
                if arr[beg_d + len_of_curr_d] == elem:
                    return beg_d + len_of_curr_d
            if arr[beg_d + len_of_curr_d - 1] == elem:
                return beg_d + len_of_curr_d - 1
        return None

    def import_func_db(self):
        result = []
        lst_from_sql = sorted(self.db_conn.read_db('', '', '', ''))
        for cur_row in lst_from_sql:
            result.append(Book(cur_row[0], cur_row[1], cur_row[2], cur_row[3], cur_row[4]))
        return result


class DBConnector:
    def __init__(self, obj_: Interface):
        self.interface = obj_
        self.db_name = self.interface.db_name
        self.db_table_name = self.interface.db_table_name
        self.conn = None
        self.curs_ = None

    @property
    def db_name(self):
        return self._db_name

    @db_name.setter
    def db_name(self, value: str):
        if value[-3:] != '.db':
            value += '.db'
        self._db_name = value
        self.interface.db_name = value

    @property
    def db_table_name(self):
        return self._db_table_name

    @db_table_name.setter
    def db_table_name(self, value: str):
        self._db_table_name = value
        self.interface.db_table_name = value

    def connect_to_the_db(self):
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            self.curs_.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.db_table_name} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    BookName TEXT,
                    BookAuthor TEXT,
                    BookYear INTEGER,
                    BookDesc TEXT);
            """)
            self.check_table()

    def check_table(self):
        try:
            self.curs_.execute(f"SELECT ID, BookName, BookAuthor, BookYear, BookDesc FROM {self.db_table_name};")
            if self.conn:
                self.interface.pop_up("database connected", self.interface)
        except sqlite3.OperationalError:
            self.db_table_name = ''
            self.interface.pop_up("Not all required columns exists in the table in database", self.interface)

    def read_db(self, nm: str, auth: str, yr: int, desc: str):
        nm = nm if nm != '' else '%'
        auth = auth if auth != '' else '%'
        yr = yr if yr != '' else '%'
        desc = desc if desc != '' else '%'
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            result = list(self.curs_.execute(f"""SELECT ID, BookName, BookAuthor, BookYear, BookDesc
                                FROM {self.db_table_name}
                                WHERE BookName LIKE '{nm}'
                                AND BookAuthor LIKE '{auth}'
                                AND BookYear LIKE '{yr}'
                                AND BookDesc LIKE '{desc}';"""))
        return result

    def append_to_db(self, nm: str, auth: str, yr: int, desc: str):
        """
        appends to the database
        :param nm: name to add
        :param auth: author to add
        :param yr: year to add
        :param desc: description to add
        :return: None
        """
        query_string = self.construct_sql_sting(nm=nm, auth=auth, yr=yr, desc=desc, type=0)
        self.change_db(query_string)

    def change_entry(self, nm: str, auth: str, yr: int, desc: str, id_: int):
        """
        changes entry in database
        :param nm: name to change
        :param auth: author to change
        :param yr: year to change
        :param desc: description to change
        :param id_: id of the record
        :return: None
        """
        query_string = self.construct_sql_sting(nm=nm, auth=auth, yr=yr, desc=desc, type=1,ID_to_change=id_)
        self.change_db(query_string)

    def remove_entry(self, id_: int):
        """
        rmove the entry from database
        :param id_: Id to remove
        :return: None
        """
        query_string = self.construct_sql_sting(type=1, ID_to_change=id_)
        self.change_db(query_string)

    def construct_sql_sting(self,
                            nm = None, auth = None, yr = None, desc = None, type = None, ID_to_change = None):
        """
        construct the query for an update method
        :param nm: name
        :param auth: author
        :param yr: year
        :param desc: deescription
        :param type: type of operation: 0 - append, 1 - change, 2 - remove
        :param ID_to_change: Id to search in database
        :return: query string
        """
        result = ""
        # Add New
        if type == 0:
            result = f"""INSERT INTO {self.db_table_name}(
                                                BookName,
                                                BookAuthor,
                                                BookYear,
                                                BookDesc)
                                            VALUES ('{nm}', '{auth}', {yr}, '{desc}');"""
        # change existing one
        elif type == 1:
            result = f"""
                    UPDATE {self.db_table_name}
                    SET BookName = '{nm}', 
                        BookAuthor = '{auth}',
                        BookYear = '{yr}',
                        BookDesc = '{desc}'
                    WHERE ID = {ID_to_change};"""
        # remove
        elif type == 2:
            result = f"""
                    DELETE FROM {self.db_table_name}
                    WHERE ID = {ID_to_change};"""
        return result

    def change_db(self, sql_: str):
        """
        updates the database
        :param sql_: query string to execute
        :return: None
        """
        with closing(sqlite3.connect(self.db_name)) as self.conn:
            self.curs_ = self.conn.cursor()
            self.curs_.execute(sql_)
            self.conn.commit()


class Book:
    def __init__(self, id: int, name: str, auth: str, year: int, desc: str):
        self._bookID =  id
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
