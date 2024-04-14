class CenteralIdentefier:
    '''
        This class is used to create a central identifier for all the classes
    '''
    def __init__(self, title, identifier):
        self.title = title
        self.identifier = identifier

    def __str__(self):
        return f"{self.title} ({self.identifier})"

    def to_dict(self):
        '''
            This function is used to convert the object into dictionary format.
        '''
        return {
            "title": self.title,
            "identifier": self.identifier
        }