from logger import BemihoLogger
from os.path import join, exists, isdir
import os, shutil

class BemihoResetProcessor:
    def __init__(self, user_input):
        self.group = user_input.group
        self.member = user_input.member
        self.output = user_input.output
        self.output_path = self.format_path()
        self.logger = BemihoLogger(self.__class__).get_logger()

    def format_path(self):
        group = self.group.kanji
        group_romaji = self.group.romaji
        member = self.member.kanji
        member_romaji = self.member.romaji
        return join(self.output, f"{group} ({group_romaji})", f"{member} ({member_romaji})")

    def start(self):
        self.logger.debug(f'Starting reset for member {self.member.kanji} ({self.member.romaji}) from {self.group.kanji} ({self.group.romaji}) located on {self.output_path}')
        if exists(self.output_path):
            self.logger.debug(f'Output path located. Resetting.')
            try:
                for file_path in os.listdir(self.output_path):
                    joined_file_path = join(self.output_path, file_path)
                    if os.path.isfile(joined_file_path):
                        os.unlink(joined_file_path)
                    elif os.path.isdir(joined_file_path):
                        shutil.rmtree(joined_file_path)
                self.logger.debug(f'Reset successful for {self.output_path}')
            except Exception:
                self.logger.error(f'Unable to reset due to an unexpected error.', exc_info=True)
        else:
            self.logger.debug(f'Output path doesn\'t exist. Terminating')