from output_processor import get_output_processor_class_for_content

from .scrapper import BemihoScrapProcessor
from .reset import BemihoResetProcessor
from .list import BemihoDataOptionsProcessor

def create_bemiho_processor(user_input):
    processor = None
    if (user_input.reset_mode):
        processor = BemihoResetProcessor(user_input)
    elif (user_input.list_mode):
        processor = BemihoDataOptionsProcessor(user_input)
    else:
        output_processor_class = get_output_processor_class_for_content(user_input.content)
        processor = BemihoScrapProcessor(user_input, output_processor_class)
    return processor