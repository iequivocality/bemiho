from logger import BemihoLogger

class BemihoUserInput:
    def __init__(self, group, member, output, content, firstpage, lastpage):
        self.group = group
        self.member = member
        self.output = output
        self.content = content
        self.firstpage = firstpage
        self.lastpage = lastpage

    def __str__(self):
        return f"Group: {self.group}\nMember: {self.member}\nOutput: {self.output}\nContent: {self.content}\nFirst Page: {self.firstpage}\nLast Page: {self.lastpage}"

class BemihoUserInputBuilder:
    def __init__(self):
        self.group = None
        self.member = None
        self.output = 'output'
        self.content = 'photos'
        self.firstpage = 1
        self.lastpage = 1
        self.logger = BemihoLogger(type(self)).get_logger()

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

    def set_lastpage(self, lastpage):
        self.lastpage = lastpage

    def build(self):
        user_input = BemihoUserInput(self.group, self.member, self.output, self.content, self.firstpage, self.lastpage)
        self.logger.debug(f'User input object created for scrapping that contains the following data:\n{user_input}')
        return user_input