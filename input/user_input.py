from logger import BemihoLogger

class BemihoUserInput:
    def __init__(self, group, member, output, content, firstpage, number_of_pages, reset_mode):
        self.group = group
        self.member = member
        self.output = output
        self.content = content
        self.firstpage = firstpage
        self.number_of_pages = number_of_pages
        self.reset_mode = reset_mode

    def __str__(self):
        return f"Group: {self.group}\nMember: {self.member}\nOutput: {self.output}\nContent: {self.content}\nFirst Page: {self.firstpage}\nNumber of Pages: {self.number_of_pages}"

class BemihoUserInputBuilder:
    def __init__(self):
        self.group = None
        self.member = None
        self.output = 'output'
        self.content = 'photos'
        self.firstpage = 1
        self.number_of_pages = 1
        self.logger = BemihoLogger(BemihoUserInputBuilder).get_logger()
        self.reset_mode = False

    def set_group(self, group):
        self.group = group

    def set_member(self, member):
        self.member = member

    def set_output(self, output):
        self.output = output

    def set_content(self, content):
        self.content = content

    def set_firstpage(self, firstpage):
        self.firstpage = firstpage

    def set_number_of_page(self, number_of_pages):
        self.number_of_pages = number_of_pages
    
    def set_reset_mode(self, reset_mode):
        self.reset_mode = reset_mode

    def build(self):
        user_input = BemihoUserInput(self.group, self.member, self.output, self.content, self.firstpage, self.number_of_pages, self.reset_mode)
        self.logger.debug(f'User input object created for scrapping that contains the following data:\n{user_input}')
        return user_input