from pathlib import Path
from importlib import import_module
from os.path import join, exists, isdir

from logger import BemihoLogger
from metadata.empty import EmptyMetadataHandler

class ScrapperOutputProcessor:
    content = ''
    def __init__(self, user_input):
        self.user_input = user_input
        file_path = Path(user_input.output).resolve()
        self.output_path = file_path
        self.member_path = self.format_path()
        self.metadata_handler = self.get_metadata_handler_class(user_input, self.member_path)
        self.logger = BemihoLogger(self.__class__).get_logger()
        group = self.user_input.group
        member = self.user_input.member
        self.logger.debug(f'Created output processor for {member.kanji} ({member.romaji}) from {group.kanji} ({group.romaji}) with path {self.member_path}')

    def get_metadata_handler_class(self, user_input, member_path):
        return EmptyMetadataHandler(user_input, member_path)

    def format_path(self):
        group = self.user_input.group.kanji
        group_romaji = self.user_input.group.romaji
        member = self.user_input.member.kanji
        member_romaji = self.user_input.member.romaji
        return join(self.output_path, f"{group} ({group_romaji})", f"{member} ({member_romaji})", self.content)

    def create_output_directory(self):
        if (not exists(self.member_path)):
            self.logger.debug(f'Folder for member path {self.member_path} doesn\'t exist. Creating folder')
            path = Path(self.member_path)
            path.mkdir(parents=True)
        self.metadata_handler.load_metadata()

    def process_blog_data(self, blog_data):
        raise NotImplementedError()