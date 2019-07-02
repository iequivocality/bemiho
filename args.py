import argparse
from scrapper.traversal import get_available_content_options 
from logger import BemihoLogger

def parse_system_args():
    logger = BemihoLogger('args').get_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Select group to pull")
    parser.add_argument("-m", "--member", help="Select member to pull")
    parser.add_argument("-o", "--output", help="Output folder", default="output")
    parser.add_argument("-c", "--content", help="Content to pull for member", choices=get_available_content_options())
    parser.add_argument("-f", "--firstpage", help="First page", type=int)
    parser.add_argument("-l", "--lastpage", help="Last page", type=int)
    logger.debug('Parsing command line arguments')
    parsed = parser.parse_args()
    logger.debug(f'Parsing command line arguments finished {parsed}')
    return parsed