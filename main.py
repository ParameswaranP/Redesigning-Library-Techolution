# This is a deliberately poorly implemented main script for a Library Management System.

import sys
import getpass # for hidden password input
from book import book
from user import user
import storage
import datetime # for noting the check out date and expected return date
from tabulate import tabulate # for pretty printing   
        
class CentralManager:
    '''
        Central Manager class for Library Management System
        It has library object which contains book_obj and user_obj
        It has storage_management object to save and load data
        It has methods to add, delete, list, search, update, checkout, checkin and track book availability
    '''
    def __init__(self):
        self.library_obj = {"book_data": [], "user_data": []}
        self.storage_management = storage.storage()
        self.library_obj = self.storage_management.load_data()
    
    def add_item(self, item, item_type=None):
        '''
            Method to add item to the library
            It takes item and item_type as input
            item_type can be books or users
            item can be book or user object
            It adds the item to the library object and save it to the storage management Json file
        '''
        if item_type == "books":
            self.library_obj["book_data"].append(item)
            item_data = item.to_dict()
            self.storage_management.save_data_dic["book_data"].update({item_data["identifier"] : item_data})
        elif item_type == "users":
            self.library_obj["user_data"].append(item)
            item_data = item.to_dict()
            self.storage_management.save_data_dic["user_data"].update({item_data["identifier"] : item_data})
        self.storage_management.save_data()
        return self.library_obj

    def delete_item(self, identifier):
        '''
            Method to delete item from the library
            It takes identifier as input
            It removes the item from the library object and save it to the storage management Json file
        '''
        remove_status = False
        for catalog, items in self.library_obj.items():
            for item in items:
                if item.identifier == identifier:
                    if isinstance(item, book):
                        if item.checked_out_by:
                            print(f"This book is checked out by a user id - {item.checked_out_by}. Checking in the book before deleting.")
                            self.checkin_book(item.checked_out_by, item.identifier)
                    elif isinstance(item, user):
                        for user_obj in self.library_obj["user_data"]:
                            if user_obj.identifier == item.identifier:
                                for checked_out_book in user_obj.checked_out_books.copy().keys():
                                    print(f"Checking in checked out book {checked_out_book} before deleting the user {item.name} with ID {item.identifier}.")
                                    self.checkin_book(item.identifier, checked_out_book)
                    items.remove(item)
                    self.storage_management.save_data_dic[catalog].pop(identifier)
                    remove_status = True
                    break
        if remove_status:
            print("Item removed successfully")
            self.storage_management.save_data()
        else:
            print("Item not found")
        # self.items = [item for item in self.items if item.identifier != identifier]
        return remove_status

    def list_items(self, item_type=None):
        '''
            Method to list items in the library
            It takes item_type as input which can be books or users
            It displays the list of items in the library
        '''
        if item_type == "books":
            book_dis_list = []
            for s_no, item in enumerate(self.library_obj["book_data"], 1):
                book_dis_list.append([s_no, item.identifier, item.title, item.author, item.checked_out_by, item.check_out_date_time, item.exp_return_date_time])
            print("List of Books in the Library: \n")
            print(tabulate(book_dis_list, headers=["S No", "ISBN", "Book Title", "Author", "Check out user ID", "Check Out At", "Expected Check In"], tablefmt="grid"))
        elif item_type == "users":
            user_dis_list = []
            for s_no, item in enumerate(self.library_obj["user_data"]):
                user_dis_list.append([s_no, item.identifier, item.name, item.checked_out_books])
            print("List of Users in the Library: \n")
            print(tabulate(user_dis_list, headers=["S No", "User ID", "User Name", "Check out Details"], tablefmt="grid"))

    def search_items(self, keyword, item_type=None):
        '''
            Method to search items in the library
            It takes keyword and item_type as input
            It searches the keyword in the library items and displays the matching items
            item_type can be books or users
        '''
        found = False
        if item_type == "books":
            for item in self.library_obj["book_data"]:
                book_dis_list = []
                if keyword.lower() in str(item).lower():
                    book_dis_list.append([1, item.identifier, item.title, item.author, item.checked_out_by, item.check_out_date_time, item.exp_return_date_time])
                    print(tabulate(book_dis_list, headers=["S No", "ISBN", "Book Title", "Author", "Check out user ID", "Check Out At", "Expected Check In"], tablefmt="grid"))
                    found = True
                    break
        elif item_type == "users":
            for item in self.library_obj["user_data"]:
                user_dis_list = []
                if keyword.lower() in str(item).lower():
                    user_dis_list.append([1, item.identifier, item.name, item.checked_out_books])
                    print(tabulate(user_dis_list, headers=["S No", "User ID", "User Name", "Check out Details"], tablefmt="grid"))
                    found = True
        if not found:
            print("No matching items found.")

    def update_item(self, identifier, title=None, author=None, password=None, item_type=None):
        '''
            Method to update item in the library
            It takes identifier, title, author, password and item_type as input
            It updates the item in the library object and save it to the storage management Json file
            item_type can be books or users
        '''
        if item_type == "books":
            for item in self.library_obj["book_data"]:
                if item.identifier == identifier:
                    if title is not None:
                        item.title = title
                    if author is not None:
                        item.author = author
                    self.storage_management.save_data_dic["book_data"].update({identifier : item.to_dict()})
                    self.storage_management.save_data()
                    break
        elif item_type == "users":
            for item in self.library_obj["user_data"]:
                if item.identifier == identifier:
                    if title is not None:
                        item.name = title
                        item.title = title
                    if password is not None:
                        item.password = password
                    self.storage_management.save_data_dic["user_data"].update({identifier : item.to_dict()})
                    self.storage_management.save_data()
                    break

    def checkout_book(self, user_id, isbn, exp_check_days):
        '''
            Method to check out book from the library
            It takes user_id, isbn and exp_check_days as input
            It checks out the book to the user and save the data in the storage management Json file
        '''
        for item in self.library_obj["book_data"]:
            if item.identifier == isbn:
                if item.checked_out_by is not None:
                    print("Book already checked out.")
                    return
                item.checked_out_by = user_id
                item.check_out_date_time = datetime.datetime.now()
                item.exp_return_date_time = (item.check_out_date_time + datetime.timedelta(days=int(exp_check_days))).strftime("%Y-%m-%d %H:%M:%S")
                item.check_out_date_time = item.check_out_date_time.strftime("%Y-%m-%d %H:%M:%S")
                for users_obj in self.library_obj["user_data"]:
                    if users_obj.user_id == user_id:
                        users_obj.checked_out_books.update({isbn: {"check_out_date_time" : item.check_out_date_time, "exp_return_date_time" : item.exp_return_date_time}})
                        break
                self.storage_management.save_data_dic["book_data"].update({isbn : item.to_dict()})
                self.storage_management.save_data_dic["user_data"].update({user_id : users_obj.to_dict()})
                self.storage_management.save_data()
                break
            else:
                print("Book not found in the library.")
                return
        print("Book checked out. Thanks for using our library service.")
    
    def checkin_book(self, user_id, isbn):
        '''
            Method to check in book to the library
            It takes user_id and isbn as input
            It checks in the book to the library and save the data in the storage management Json file
        '''
        for users_obj in self.library_obj["user_data"]:
            if users_obj.user_id == user_id:
                if isbn not in users_obj.checked_out_books.keys():
                    print("User has not checked in this book.")
                    return
                users_obj.checked_out_books.pop(isbn)
                for item in self.library_obj["book_data"]:
                    if item.identifier == isbn:
                        item.checked_out_by = None
                        item.check_out_date_time = None
                        item.exp_return_date_time = None
                        self.storage_management.save_data_dic["book_data"].update({isbn : item.to_dict()})
                        self.storage_management.save_data_dic["user_data"].update({user_id : users_obj.to_dict()})
                        self.storage_management.save_data()
                        print("Book checked in. Thanks for using our library service")
                        break

    def track_book_avilability(self, isbn):
        '''
            Method to track book availability in the library
            It takes isbn as input
            It checks the book availability in the library and displays the status
        '''
        for item in self.library_obj["book_data"]:
            if item.identifier == isbn:
                if item.checked_out_by:
                    print(f"Book is checked out by user {item.checked_out_by} and we can expect it back by {item.exp_return_date_time}")
                    return
                else:
                    print("Book is available in the library.")
                    return
        print("Book not avilable in our library.")
     
def login(center_manager):
    '''
        Method to authenticate user login
        It takes center_manager as input to access the storage management object
        It takes username and password as input
        It checks the username and password in the storage management Json file
        It returns authenticated status and user id
    '''
    username = input("Enter username: ")
    logged_in = False
    for id, user_data in center_manager.storage_management.save_data_dic["user_data"].items():
        if username == user_data["name"]:
            password = getpass.getpass(prompt="Enter password: ")
            if storage.cipher_suite.decrypt(user_data["password"].encode()).decode() == password:
                print("Logged in successfully.")
                logged_in = True
                return True, id
    if not logged_in:
        print("Invalid username or password. Please try again.")
        return False, None


def main_menu():
    '''
        Method to display main menu options
    '''
    menu_options = [
        "Add Book", "Update Book", "Delete Book", "List Books", "Search Book",
        "CheckOut Book", "CheckIn Book", "Track Book Availability",
        "Add User", "Update User", "Delete User", "List Users", "Search User", "Exit"]
    print("\nMain Menu")
    print_menu = []
    for i, option in enumerate(menu_options, 1):
        print_menu.append([i, option])
    print(tabulate(print_menu, headers=["Option", "Action"], tablefmt="grid"))
    choice = input("Enter choice: ")
    return choice

def main():
    '''
        Main method to run the Library Management System
    '''
    center_manager = CentralManager()
    # while not authenticated:
    print("\nWelcome to the Library Management System.")
    
    while True:
        choice = main_menu()
        if choice == '1': # add book
            while True:
                isbn = input("Enter ISBN or # for main menu: ")
                if isbn in center_manager.storage_management.save_data_dic["book_data"].keys():
                    print("Book with the given ISBN already exists. kindly enter a different ISBN")
                elif isbn == "#":
                    break
                else:
                    title = input("Enter title: ")
                    author = input("Enter author: ")
                    
                    book_obj = book(title, author, isbn)
                    center_manager.add_item(book_obj, "books")
                    print("Book added Sucessfully.")
                    break
        elif choice == '2': # update book
            while True:
                book_find = False
                identifier = input("Enter ISBN of the book to update or # for main menu: ")
                if identifier == "#":
                    break
                for item in center_manager.library_obj["book_data"]:
                    if item.identifier == identifier:
                        print(f"Book with following data found \nTitle - {item.title} \nAuthor Name- {item.author}")
                        book_find = True
                        break
                if not book_find:
                    print("Book not found kindly try with another ISBN.")
                    continue
                else:
                    print("Editable fields: Book tile and author name")
                    title = input("Enter title (leave blank to skip) : ")
                    if title == "":
                        title = None
                    author = input("Enter author (leave blank to skip) : ")
                    if author == "":
                        author = None
                    if not title and not author:
                        print("No changes made.")
                        continue
                    center_manager.update_item(identifier, title=title, author=author, item_type="books") 
                    print("Book updated sucessfully. Redirecting to main menu.")   
                    break     
        elif choice == '3': # delete book
            while True:
                identifier = input("Enter ISBN of the book to delete or # for main menu: ")
                if identifier == "#":
                    break
                center_manager.delete_item(identifier)
        elif choice == '4': # list book
            center_manager.list_items("books")
            input("Press Any key for main menu ...")
        elif choice == '5': # search book
            while True:
                keyword = input("Enter book name or ISNB to search for a book or # for main menu: ")
                if keyword == "#":
                    break
                center_manager.search_items(keyword, "books")
        elif choice == '6': # check out book
            print("To check out a book Please login.")
            authenticated, login_user_id = login(center_manager)
            if authenticated:
                while True:
                    item_identifier = input("Enter ISBN of the book to check out or # for main menu: ")
                    if item_identifier == "#":
                        break
                    number_of_day_required = input("Enter number of days to keep the book or # for main menu: ")
                    if number_of_day_required == "#":
                        break
                    center_manager.checkout_book(login_user_id, item_identifier, exp_check_days=number_of_day_required)
            else:
                input("Login failed!!!. \nPress Any key for main menu ...")
        elif choice == '7': # check out book
            print("To check in Please log in.")
            authenticated, login_user_id = login(center_manager)
            if authenticated:
                while True:
                    item_identifier = input("Enter ISBN of the book to check IN or # for main menu: ")
                    if item_identifier == "#":
                        break
                    center_manager.checkin_book(login_user_id, item_identifier)
            else:
                input("Login failed!!!. \nPress Any key for main menu ...")
        elif choice == '8': # track book avilability
            while True:
                item_identifier = input("Enter ISBN of the book to track or # for main menu: ")
                if item_identifier == "#":
                    break
                center_manager.track_book_avilability(item_identifier)
        elif choice == '9': # Add user
            while True:
                user_id = input("Enter user ID or # for main menu: ")
                if user_id in center_manager.storage_management.save_data_dic["user_data"].keys():
                    print("User ID already taken kindly enter a different user id or update the existing user.")
                    continue
                elif user_id == "#":
                    break
                else:
                    name = input("Enter user name: ")
                    password = getpass.getpass(prompt="Enter password: ")
                    e_password = storage.cipher_suite.encrypt(password.encode()).decode()
                    user_obj = user(name, user_id, e_password)
                    center_manager.add_item(user_obj, "users")
                    print("User added sucessfully.")
                    break
        elif choice == '10': # update user
            while True:
                user_find = False
                identifier = input("Enter user id of the user to update or # for main menu: ")
                if identifier == "#":
                    break
                for item in center_manager.library_obj["user_data"]:
                    if item.identifier == identifier:
                        print(f"User Name - {item.name} \nUser ID - {item.identifier}")
                        user_find = True
                        break
                if not user_find:
                    print("User not found.")
                    continue
                else:
                    print("Editable fields: name, password")
                    title = input("Enter user name to change (leave blank to skip) : ")
                    if title == "":
                        title = None
                    password = getpass.getpass(prompt="Enter password to be changed (leave blank to skip) : ")  
                    if password == "":
                        password = None              
                    if not title and not password:
                        print("No changes made.")
                        continue
                    center_manager.update_item(identifier, title=title, password=password, item_type="users")
                    print("User updated sucessfully. Redirecting to main menu.")
                    break                  
        elif choice == '11': # delete user
            while True:
                identifier = input("Enter User ID of the user to delete a user or # for main menu: ")
                if identifier == "#":
                    break
                center_manager.delete_item(identifier)
        elif choice == '12': # list users
            center_manager.list_items("users")
            input("Press Any key for main menu ...")
        elif choice == '13': # search book
            while True:
                keyword = input("Enter user name or User ID to search for a user or # for main menu: ")
                if keyword == "#":
                        break
                center_manager.search_items(keyword, "users")
        elif choice == '14': # exit
            print("Thank you for visiting the library. We hope to see you again soon!")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
