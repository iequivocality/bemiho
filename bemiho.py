from bs4 import BeautifulSoup
from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper
from input.accept_input import get_user_input
from scrapper import BemihoScrapProcessor
from logger import BemihoLogger

from output_processor import get_output_processor_class_for_content

from output_processor.exceptions import OutputProcessorNotFound
from scrapper.traversal.exceptions import TraversalClassNotFound

if __name__ == '__main__':
    logger = BemihoLogger('bemiho').get_logger()
    try:
        logger.debug('Starting Bemiho.')
        user_input = get_user_input()
        output_processor_class = get_output_processor_class_for_content(user_input.content)
        processor = BemihoScrapProcessor(user_input, output_processor_class)
        processor.start()
    except OutputProcessorNotFound as oe:
        logger.error(oe.message, exc_info=True)
    except TraversalClassNotFound as te:
        logger.error(te.message, exc_info=True)
    except Exception as e:
        logger.error(f'Uncaught exception occurred', exc_info=True)
    finally:
        logger.debug('Stopped Bemiho.')

