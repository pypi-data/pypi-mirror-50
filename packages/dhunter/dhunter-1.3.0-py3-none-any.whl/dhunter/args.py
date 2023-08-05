# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""

import argparse
import os
from argparse import RawDescriptionHelpFormatter

from dhunter.const import Const
from dhunter.log import Log


class Args(object):
    """Handles command line arguments"""

    # noinspection PyTypeChecker
    @staticmethod
    def parse_args() -> argparse.Namespace:
        """Parses command line arguments
        """
        parser = argparse.ArgumentParser(
                prog=Const.APP_NAME.lower(),
                description='{app} v{v}\n'.format(app=Const.APP_NAME, v=Const.APP_VERSION) +
                            'Written by Marcin Orlowski <mail@marcinOrlowski.com>',
                formatter_class=RawDescriptionHelpFormatter)

        group = parser.add_argument_group('Directories')
        group.add_argument(
                metavar='DIR', action='store', dest='src_dirs', nargs='+',
                help='Directories to work on')

        group = parser.add_argument_group('Commands')
        group.add_argument('-d', '-duplicates', '--duplicates',
                           action='store_true', dest='duplicates',
                           help='Lists all duplicates detected across specified dirs')
        group.add_argument('-s', '-stats', '--stats',
                           action='store_true', dest='cmd_stats',
                           help='Show more info about scanned data')

        group = parser.add_argument_group('State files')
        group.add_argument('-state', '--state',
                           metavar='FILE', action='store', dest='state_file', nargs=1,
                           help='Persistent hash storage cache file to use.')

        group = parser.add_argument_group('Sorting and results limit')
        group.add_argument('-sort', '--sort',
                           metavar='MODE', action='store', dest='sort_by', nargs=1,
                           help='Results sorting order. Allowed modes are: ' + ', '.join(Const.ALLOWED_SORT_VALUES))
        group.add_argument('-r', '-reverse', '--reverse',
                           action='store_true', dest='reverse_order',
                           help='Reverses order of displayed data.')
        group.add_argument('-l', '-limit', '--limit',
                           metavar='COUNT', action='store', dest='limit', nargs=1, type=int,
                           help='Limit number of shown results to given count. '
                                'Default is 0, which means no limits.')

        group.add_argument('-min', '--min',
                           metavar='SIZE', action='store', dest='min_size', nargs=1, type=str,
                           help='Min file size threshold. Files smaller than SIZE will be ignored. '
                                'Supported format <VAL><UNIT> where val is positive integer, and '
                                'unit is one letter (case insensitive): b for bytes, k for KiB, '
                                'm for MiB, g for GiB and t for TiB. i.e. "1024" = "1024b" = "1k". '
                                'Default is 0, which means no limits.')
        group.add_argument('-max', '--max',
                           metavar='SIZE', action='store', dest='max_size', nargs=1, type=str,
                           help='Max file size threshold. Files bigger than SIZE will be ignored. '
                                'Supported format <VAL><UNIT> where val is positive integer, and '
                                'unit is one letter (case insensitive): b for bytes, k for KiB, '
                                'm for MiB, g for GiB and t for TiB. i.e. "1024" = "1024b" = "1k". '
                                'Default is 0, which means no limits.')

        group = parser.add_argument_group('Misc')
        group.add_argument('-rehash', '--rehash',
                           action='store_true', dest='force_rehash',
                           help='Ignores file hash cache files and re-does all the hashes.')
        group.add_argument('-v', '--verbose',
                           action='store_true', dest='verbose',
                           help='Enables verbose output.')
        group.add_argument('--version', action='version',
                           version='{app} v{v}'.format(app=Const.APP_NAME, v=Const.APP_VERSION))

        group = parser.add_argument_group('Developer tools')
        group.add_argument('-debug', '--debug',
                           action='store_true', dest='debug',
                           help='Enables debug mode.')
        group.add_argument('-dd', '-debug-verbose', '--debug-verbose',
                           action='store_true', dest='debug_verbose',
                           help='Enables verbose debug output (implies --debug).')

        # this trick is to enforce stacktrace in case parse_args() fail (which should normally not happen)
        # old_config_debug = config.debug
        # if not config.debug:
        #     config.debug = True

        args = parser.parse_args()

        # config.debug = old_config_debug

        # we need at least one command set
        # if args.save_state is None and args.load_state is None and args.src_dirs is None:
        #     Log.abort('No action specified')

        if args.debug and os.getenv('PYTHONDONTWRITEBYTECODE') is None:
            Log.e([
                'Creation of *.pyc files is enabled in your current environment.',
                'This affects Log.d() calls and may produce invalid stacktrace,',
                'and incorrect file and line number shown during runtime.',

                'To disable this, set env variable:',
                '   export PYTHONDONTWRITEBYTECODE=1',
            ])

        return args
