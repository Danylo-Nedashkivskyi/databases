class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def menu(self):
        exit = False
        while not exit:
            print("""
1 - Show contents of a table
2 - Show contents of all tables
3 - Insert record
4 - Modify record
5 - Delete record
6 - Find record
7 - Randomize data
8 - Exit
            """)
            choice = input("Input: ")
            try:
                choice = int(choice)
            except:
                print("Invalid input, please try again")
                continue
            if choice == 1:
                self.view.table_list()
                table = input("Choose a table: ")
                try:
                    table = int(table)
                except:
                    print("Invalid input, please try again")
                    continue
                if self.model.table_type(table):
                    print("Selected number does not correspond to a table, please try again")
                    continue
                items = self.model.read_entries()
                self.view.show_table(table, items)
            elif choice == 2:
                for i in range(1, 4):
                    self.model.table_type(i)
                    items = self.model.read_entries()
                    self.view.show_table(i, items)
            elif choice == 3:
                self.view.table_list()
                table = input("Choose a table: ")
                try:
                    table = int(table)
                except:
                    print("Invalid input, please try again")
                    continue
                if self.model.table_type(table):
                    print("Selected number does not correspond to a table, please try again")
                    continue
                print("Input data that you wish to insert:")
                items = list()
                for cat in self.view.categories[table]:
                    print("{} = ".format(cat), end="")
                    items.append(input())
                try:
                    self.model.create_entry(items)
                    print("Entry successfully created:")
                    self.view.show_entry(self.model.read_entry(items[0]))
                except:
                    print("Invalid data - couldn't create entry")
            elif choice == 4:
                self.view.table_list()
                table = input("Choose a table: ")
                try:
                    table = int(table)
                except:
                    print("Invalid input, please try again")
                    continue
                if self.model.table_type(table):
                    print("Selected number does not correspond to a table, please try again")
                    continue
                print("Input the name of the entry that you wish to modify: ", end="")
                primkey = input()
                items = list()
                print("Input data that you wish to insert:")
                for cat in self.view.categories[table]:
                    print("{} = ".format(cat), end="")
                    items.append(input())
                try:
                    self.model.update_entry(primkey, items)
                    print("Entry successfully updated:")
                    self.view.show_entry(self.model.read_entry(items[0]))
                except:
                    print("Invalid data - couldn't update entry")
            elif choice == 5:
                self.view.table_list()
                table = input("Choose a table: ")
                try:
                    table = int(table)
                except:
                    print("Invalid input, please try again")
                    continue
                if self.model.table_type(table):
                    print("Selected number does not correspond to a table, please try again")
                    continue
                primkey = input("Input the name/ID of the entry that you wish to delete: ")
                try:
                    self.model.delete_entry(primkey)
                    print("Entry successfully deleted.")
                except:
                    print("Invalid data - couldn't delete entry")
            elif choice == 6:
                print("""
Choose the relation:
1 - Email by User
2 - Folder by User
3 - Email by Folder
                """)
                rel = input("Input: ")
                try:
                    rel = int(rel)
                except:
                    print("Invalid input, please try again")
                    continue
                if rel < 1 or rel > 3:
                    print("Invalid input, please try again")
                primkey = input("Input the username/folder name related to the entry that you wish to find: ")
                try:
                    entries = self.model.find_entries(primkey, rel)
                    if entries:
                        print("Entries found:")
                        self.view.show_entries(entries)
                    else:
                        print("No entries found")
                except:
                    print("Invalid data - couldn't find entries")
            elif choice == 7:
                self.view.table_list()
                table = input("Choose a table: ")
                try:
                    table = int(table)
                except:
                    print("Invalid input, please try again")
                    continue
                if self.model.table_type(table):
                    print("Selected number does not correspond to a table, please try again")
                    continue
                n = input("Input number of rows to be generated: ")
                try:
                    n = int(n)
                except:
                    print("Invalid input, please try again")
                    continue
                try:
                    self.model.randomize(n)
                except:
                    print("Unknown error during randomization")
            elif choice == 8:
                exit = True
