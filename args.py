import argparse
from scrapper.traversal import get_available_content_options 
from logger import BemihoLogger

def parse_system_args():
    logger = BemihoLogger(parse_system_args).get_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Select group to pull")
    parser.add_argument("-m", "--member", help="Select member to pull")
    parser.add_argument("-o", "--output", help="Output folder", default="output")
    parser.add_argument("-c", "--content", help="Content to pull for member", choices=get_available_content_options(), type=str.lower)
    parser.add_argument("-f", "--firstpage", help="First page", type=int)
    parser.add_argument("-n", "--number", help="Number of pages", type=int)
    parser.add_argument("--reset", help="Resets saved data from idol's blog", action='store_true')
    parser.add_argument("--list", help="Lists all groups and supported members", action='store_true')
    logger.debug('Parsing command line arguments')
    parsed = parser.parse_args()
    logger.debug(f'Parsing command line arguments finished {parsed}')
    return parsed