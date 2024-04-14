import json
import os
from book import BookManagement
from user import UserManagement
from cryptography.fernet import Fernet  # for encripting the password

# Generate a key for encryption and decryption
# key = Fernet.generate_key()
# print(key)
our_key = b'AakxkKGGGNLTYL3KnpdGe-k3DvaT1iAepzxHafVdfn0=' # encription key
cipher_suite = Fernet(our_key)


class StorageManagement:
    '''
        StorageManagement class is used to load and save the data in json file.
        It has save_data_dic which holds the library_obj respective data in dictionary format and then saved in json.
    '''
    def __init__(self):
        self.items = []
        self.library_obj = {"book_data": [], "user_data": []}
        self.save_data_dic = {"book_data": {}, "user_data": {}}

    def load_data(self):
        '''
            This function is used to load the data from json file and then store it in library_obj.
        '''
        if os.path.exists("library_data.json"):
            with open("library_data.json", "r") as file:
                data = json.load(file)
                # print("loading data from json : \n", data)
                for category, items in data.items():
                    if category == "book_data":
                        for identifier, item_data in items.items():
                            item = BookManagement(item_data["title"], item_data["author"], item_data["identifier"], item_data["checked_out_by"], item_data["check_out_date_time"], item_data["exp_return_date_time"])
                            self.library_obj["book_data"].append(item)
                            self.save_data_dic["book_data"].update({identifier : item_data})
                    else:
                        for identifier, item_data in items.items():
                            item = UserManagement(item_data["title"], identifier, item_data["password"], item_data["checked_out_books"])
                            self.library_obj["user_data"].append(item)
                            self.save_data_dic["user_data"].update({identifier : item_data})
                            # self.save_data_dic["user_data"].append(item_data)
        # print("Data loaded in library_obj: \n", self.library_obj)
        return self.library_obj

    def save_data(self, item_type=None):
        '''
            This function is used to save the data in json file.
        '''
        with open("library_data.json", "w") as file:
            json.dump(self.save_data_dic, file, indent=4)
