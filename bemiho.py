import sys
import time

from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound, PageNumberNotDigits, InvalidContentInput, NumberOfPageShouldBeAtLeastOne
from logger import BemihoLogger 

from output_processor.exceptions import OutputProcessorNotFound
from scrapper.traversal.exceptions import TraversalClassNotFound

from processor import create_bemiho_processor
from utilities.text import seconds_to_minutes_format

if __name__ == '__main__':
    logger = BemihoLogger('bemiho').get_logger()
    start = time.time()
    try:
        logger.info('Starting Bemiho.')
        user_input = get_user_input()
        processor = create_bemiho_processor(user_input)
        processor.start()
    except (JSONDataNotFound, PageNumberNotDigits, NumberOfPageShouldBeAtLeastOne, InvalidContentInput):
        logger.error("There were exceptions in acquiring data", exc_info=True)
    except OutputProcessorNotFound as oe:
        logger.error(oe.message, exc_info=True)
    except TraversalClassNotFound as te:
        logger.error(te.message, exc_info=True)
    except KeyboardInterrupt as ke:
        logger.debug("User stopped the application.")
    except Exception as e:
        logger.error('Uncaught exception occurred', exc_info=True)
    finally:
        end = time.time()
        total_seconds = (end - start)
        logger.debug('Stopped Bemiho.')
        logger.info(f'Duration: {seconds_to_minutes_format(total_seconds)}')
