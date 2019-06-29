from output_processor.file_handler import OutputFolderHandler

class ScrapperOutputProcessor:
    def __init__(self, user_input, metadata_handler):
        self.user_input = user_input
        self.metadata_handler = metadata_handler
        self.output_folder_handler = OutputFolderHandler(self.user_input)
        self.output_folder_handler.create_member_directory()
    
    def process_blog_data(self, blog_datum):
        print(blog_datum.contents)

    
    
