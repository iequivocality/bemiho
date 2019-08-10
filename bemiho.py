import sys
import time

from input.accept_input import get_user_input
from input.exceptions import JSONDataNotFound, PageNumberNotDigits, InvalidContentInput, NumberOfPageShouldBeAtLeastOne
from processor.scrapper import BemihoScrapProcessor
from logger import BemihoLogger

from output_processor import get_output_processor_class_for_content

from output_processor.exceptions import OutputProcessorNotFound
from scrapper.traversal.exceptions import TraversalClassNotFound

from processor.reset import BemihoResetProcessor

from json_extractor.reader import JSONExtractor
from json_extractor.mapper import GroupJSONObjectMapper, MemberJSONObjectMapper

if __name__ == '__main__':
    logger = BemihoLogger('bemiho').get_logger()
    start = time.time()
    try:
        logger.info('Starting Bemiho.')
        user_input = get_user_input()
        if (user_input.reset_mode):
            reset_processor = BemihoResetProcessor(user_input)
            reset_processor.start()
        elif (user_input.list_mode):
            extractor = JSONExtractor('index/index.idols', GroupJSONObjectMapper())
            group_data = extractor.extract()
            for group in group_data:
                print(f'({group.index}) {group.romaji} - {group.kanji}')
                extractor = JSONExtractor(f'index/{group.index_file}', MemberJSONObjectMapper())
                member_data = extractor.extract()
                for member in member_data:
                    print(f'    ({member.index}) {member.romaji} - {member.kanji}')
            
        else:
            output_processor_class = get_output_processor_class_for_content(user_input.content)
            processor = BemihoScrapProcessor(user_input, output_processor_class)
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
        logger.info(f'Duration: {int(total_seconds)}s')
