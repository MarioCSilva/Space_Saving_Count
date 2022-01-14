import sys
import logging
import argparse
from tests import Test


class Main:
    def __init__(self):
        Test(*self.check_arguments())


    def usage(self):
        print("Usage: python3 main.py\
            \n\t-f <File Name for Counting Words: str>\
            \n\t-e <Epsilon Value for Space Saving Count: int>\
            \n\t-e <Epsilon Value for Space Saving Count: int>")

        sys.exit()


    def check_arguments(self):
        arg_parser = argparse.ArgumentParser(
            prog="Approximate Counter",
            usage=self.usage
        )
        arg_parser.add_argument('-help', action='store_true')
        arg_parser.add_argument('-file_name', nargs=1, type=str, default=['../datasets/en_bible.txt'])
        arg_parser.add_argument('-epsilon', nargs=1, type=int, default=[0.01])

        try:
            args = arg_parser.parse_args()
        except:
            self.usage()

        if args.help:
            self.usage()

        return args.file_name[0], args.epsilon[0]


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    main = Main()