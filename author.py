class Author:
    def __init__(self, name, biography):
        self.__name = name
        self.__biography = biography
    
    # Getters for author details
    def get_name(self):
        return self.__name
    
    def get_biography(self):
        return self.__biography
