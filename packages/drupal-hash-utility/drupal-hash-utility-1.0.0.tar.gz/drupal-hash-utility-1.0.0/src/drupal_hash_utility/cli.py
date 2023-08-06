from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from logging import DEBUG
from logging import INFO
from logging import basicConfig
from logging import info
from sys import argv
from time import time

from drupal_hash_utility import DrupalHashUtility

__version__ = '1.0.0'
__cli_name__ = 'drupal-hash-utility'

LOG_MSG_FMT = 'pid(%(process)d) | %(asctime)s | %(levelname)s >> %(message)s'
LOG_DATE_FMT = '%d-%b-%Y %H:%M:%S'


def parse_args(*args, **kwargs):
    start_time = time()

    class FormatterClass(RawTextHelpFormatter):
        def __init__(self, *a, **kw):
            super(RawTextHelpFormatter, self).__init__(*a, **kw)

            self._width = 100
            self._max_help_position = 50

    parser = ArgumentParser(
        description='A hashing utility built from Drupal7 specification.',
        prog=__cli_name__,
        epilog='welcome to thaxoo...',
        formatter_class=FormatterClass,
        add_help=False
    )

    parser._positionals.title = 'Required'
    parser._optionals.title = 'Optional'

    subparsers = parser.add_subparsers(
        dest='subparsers'
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        help='Display this help message.'
    )

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=f'{__cli_name__} {__version__}',
        help='Output app name and version.'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='Display verbose output; can be used more than once for greater verbosity.'
    )

    encode_parser = subparsers.add_parser(
        'encode',
        help='Encode the given password into a Drupal7 hash.',
        formatter_class=FormatterClass,
        add_help=False
    )

    encode_parser.add_argument(
        '-h', '--help',
        action='help',
        help='Display this help message.'
    )

    encode_parser.add_argument(
        '-p', '--password',
        action='store',
        help='Encode the given password.',
        dest='password',
        required=True
    )

    verify_parser = subparsers.add_parser(
        'verify',
        help='Verify the given password and Drupal7 hash cryptographically match.',
        formatter_class=FormatterClass,
        add_help=False
    )

    verify_parser.add_argument(
        '-h', '--help',
        action='help',
        help='Display this help message.'
    )

    verify_parser.add_argument(
        '-p', '--password',
        action='store',
        help='The password you want to verify the hash against.',
        dest='password',
        required=True
    )

    verify_parser.add_argument(
        '-d', '--drupal-hash',
        action='store',
        help='The hash you want to verify the password against.',
        dest='hash',
        required=True
    )

    summary_parser = subparsers.add_parser(
        'summary',
        help='Generate a summary of a given hash.',
        formatter_class=FormatterClass,
        add_help=False
    )

    summary_parser.add_argument(
        '-h', '--help',
        action='help',
        help='Display this help message.'
    )

    summary_parser.add_argument(
        '-d', '--drupal-hash',
        action='store',
        help='Hash you want to generate a summary for.',
        dest='hash',
        required=True
    )

    parsed = parser.parse_args()

    if parsed.verbose is not None:
        if parsed.verbose == 1:
            basicConfig(format=LOG_MSG_FMT, datefmt=LOG_DATE_FMT, level=INFO)
        elif parsed.verbose > 1:
            basicConfig(format=LOG_MSG_FMT, datefmt=LOG_DATE_FMT, level=DEBUG)

    main(parsed)

    info(f'Processed in {round(time() - start_time)} seconds.')


def main(parsed):
    if parsed.subparsers == 'encode' and parsed.password:
        print(DrupalHashUtility().encode(parsed.password))
    elif parsed.subparsers == 'verify' and parsed.password and parsed.hash:
        print(DrupalHashUtility().verify(parsed.password, parsed.hash))
    elif parsed.subparsers == 'summary' and parsed.hash:
        print(DrupalHashUtility().summary(parsed.hash))


if __name__ == "__main__":
    parse_args(*argv)
