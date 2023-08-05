# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import argparse

from ..core.args_base import ArgsBase
from ..core.const import Const


class Args(ArgsBase):
    """Handles command line arguments"""

    def _get_tool_name(self) -> str:
        return 'dscan'

    # noinspection PyTypeChecker
    def parse_args(self) -> argparse.Namespace:
        """Parses command line arguments
        """
        parser = self._get_parser()

        group = parser.add_argument_group('Project')
        group.add_argument('-db', '--db',
                           metavar='DB_FILE', action='store', dest='db_file', nargs=1,
                           help='Name of project database file to create.')

        group.add_argument(
            metavar='DIR', action='store', dest='src_dirs', nargs='+',
            help='Directories to process.')

        group = parser.add_argument_group('Misc')
        group.add_argument('-r', '-rehash', '--rehash',
                           action='store_true', dest='force_rehash',
                           help='Ignores existing file hash cache files ({dot}) and regenerates '
                                'all the hashes.'.format(dot=Const.FILE_DOT_DHUNTER))
        group.add_argument('-cmd', '--cmd', '--command',
                           action='store', dest='command', nargs=1, metavar="COMMAND", default=Const.CMD_SCAN,
                           help='Action to execute. Commands are: %s. ' % ', '.join(Const.SCANNER_CMDS) +
                                'Default command is %s' % Const.CMD_SCAN)
        group.add_argument('-ro', '--ro', '--read-only',
                           action='store_true', dest='dont_save_dot_file',
                           help='Tells the scanner to treat all the folders as read only and do not '
                                'write cache file ({dot})'.format(dot=Const.FILE_DOT_DHUNTER))
        group.add_argument('-rp', '--rp', '--relative-paths',
                           action='store_true', dest='relative_paths',
                           help='Store paths in DB as relative instead of absolute.')
        group.add_argument('-nr', '--nr', '--no-recursive',
                           action='store_true', dest='no_recursive',
                           help='Do not scan subdirectories.')

        group = self._add_filter_option_group(parser)
        group.add_argument('-exdir', '--exdir',
                           metavar='REGEXP', action='append', dest='exclude_dir_regexps', nargs=1, type=str,
                           help='Exclude directories (paths) matching specified regular expression. '
                                'Option can be used multiple times for multiple patters. Also always quote '
                                'your patterns to prevent shell expansion.')
        group.add_argument('-exfile', '--exfile',
                           metavar='REGEXP', action='append', dest='exclude_file_regexps', nargs=1, type=str,
                           help='Exclude filenames matching specified regular expression. '
                                'Option can be used multiple times for multiple patters. Also always quote '
                                'your patterns to prevent shell expansion.')

        self._add_other_option_group(parser)

        # this trick is to enforce stacktrace in case parse_args() fail (which should normally not happen)
        # old_config_debug = config.debug
        # if not config.debug:
        #     config.debug = True

        args = parser.parse_args()

        # config.debug = old_config_debug

        # we need at least one command set
        # if args.save_state is None and args.load_state is None and args.src_dirs is None:
        #     Log.abort('No action specified')

        self._debug_check(args)

        return args
