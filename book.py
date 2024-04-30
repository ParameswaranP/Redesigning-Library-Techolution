from models import CenteralIdentefier


class book(CenteralIdentefier):
    '''
        BookManagement class is used to create a book object.
        It has the information of book like title, author, isbn, checked_out_by, check_out_date_time, exp_return_date_time.
    '''
    def __init__(self, title, author, isbn, checked_out_by=None, check_out_date_time=None, exp_return_date_time=None):
        super().__init__(title, isbn)
        self.author = author
        self.isbn = isbn
        self.title = title
        self.checked_out_by = checked_out_by
        self.check_out_date_time = check_out_date_time
        self.exp_return_date_time = exp_return_date_time

    def __str__(self):
        return f"{super().__str__()} by {self.author}, Title {self.title} and ISBN {self.isbn}"

    def to_dict(self):
        '''
            This function is used to convert the book object into dictionary format.
        '''
        data = super().to_dict()
        data["author"] = self.author
        data["title"] = self.title
        data["isbn"] = self.isbn
        data["checked_out_by"] = self.checked_out_by
        data["check_out_date_time"] = self.check_out_date_time
        data["exp_return_date_time"] = self.exp_return_date_time
        
        return data