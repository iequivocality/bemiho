import argparse
from const import CONTENT_CHOICES

def parse_system_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", help="Select group to pull")
    parser.add_argument("-m", "--member", help="Select member to pull")
    parser.add_argument("-o", "--output", help="Output folder", default="output")
    parser.add_argument("-c", "--content", help="Content to pull for member", choices=CONTENT_CHOICES)
    parser.add_argument("-f", "--firstpage", help="First page", type=int)
    parser.add_argument("-l", "--lastpage", help="Last page", type=int)
    return parser.parse_args()