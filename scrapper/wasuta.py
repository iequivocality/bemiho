from scrapper import Scrapper

class WasutaScrapper(Scrapper):
    code = 'Wasuta'
    def __init__(self, user_input, page_number, traversal):
        super().__init__(user_input, page_number, traversal)