tables = {
    1: "Email",
    2: "Folder",
    3: "User"
}

class View(object):
    categories = {
        1: ("ID", "Title", "Arrival Date", "Assoc. Folder", "Assoc. User"),
        2: ("Name", "ID", "Assoc. User"),
        3: ("Username", "Creation date")
    }

    @staticmethod
    def table_list():
        print("""
        1 - Email
        2 - Folder
        3 - User
        """)

    @staticmethod
    def show_entry(item):
        print("* {}".format(item))

    @staticmethod
    def show_entries(items):
        for item in items:
            print("* {}".format(item))

    @staticmethod
    def show_table(table_type, items):
        print("===== TABLE {} =====".format(tables[table_type]))
        for item in items:
            print("* {}".format(item))