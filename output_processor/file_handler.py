import os
from utilities.file import create_directory

from os.path import join, exists, isdir

#this is temporary
from scrapper.traversal import get_available_content_options

class OutputFolderHandler:
    def __init__(self, user_input):
        self.user_input = user_input
        self.output_path = join(os.getcwd(), user_input.output)
        self.content_folders = {}

    def create_main_directory(self):
        output_path = self.output_path
        create_directory(output_path)
    
    def create_group_directory(self):
        output_path = self.output_path
        if (not exists(output_path)):
            self.create_main_directory()
            self.create_group_directory()
        else:
            group = self.user_input.group.kanji
            group_path = join(output_path, group)
            # print(group_path)
            create_directory(group_path)
            self.group_path = group_path

    def create_member_directory(self):
        output_path = self.output_path
        group = self.user_input.group.kanji
        group_path = join(output_path, group)
        if (not exists(group_path)):
            self.create_group_directory()
            self.create_member_directory()
        else:
            member = self.user_input.member.kanji
            member_path = join(group_path, member)
            create_directory(member_path)
            self.member_path = member_path
            self.create_directory_for_members()

    def create_directory_for_members(self):
        content_options = get_available_content_options()
        for cont_opt in content_options:
            self.content_folders[cont_opt] = join(self.member_path, cont_opt)
            if (not exists(self.content_folders[cont_opt])):
                create_directory(self.content_folders[cont_opt])
    
    def get_directory_for_member_subdirectories(self, content):
        return self.content_folders[content]

    def get_member_path(self):
        return self.member_path