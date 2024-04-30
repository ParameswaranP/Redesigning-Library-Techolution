from models import CenteralIdentefier


class user(CenteralIdentefier):
    '''
        user class is used to create a user object.
        It has the information of user like name, user_id, password, checked_out_books.
    '''
    def __init__(self, name, user_id, password, checked_out_books={}):
        super().__init__(name, user_id)
        self.name = name
        self.user_id = user_id
        self.password = password
        self.checked_out_books = checked_out_books

    def __str__(self):
        return f"{super().__str__()}"

    def to_dict(self):
        '''
            This function is used to convert the user object into dictionary format.
        '''
        data = super().to_dict()
        data["name"] = self.name
        data["user_id"] = self.user_id
        data["password"] = self.password
        data["checked_out_books"] = self.checked_out_books
        return data
