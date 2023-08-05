# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import argparse
from .const import Const


class ArgsBase(object):

    def _get_tool_name(self) -> str:
        """
        Returns name of invoked utility. This string is only used when help
        string is going to be shown, so it mention the right name of package tool
        handling these options.

        :return:
        """
        return Const.APP_NAME.lower()

    def _get_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog=self._get_tool_name(),
            description='{app} v{v}\n'.format(app=Const.APP_NAME, v=Const.APP_VERSION) +
                        'Written by Marcin Orlowski, See ' + Const.APP_URL,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        return parser

    def _add_filter_option_group(self, parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
        group = parser.add_argument_group('Filters')
        group.add_argument('-min', '--min',
                           metavar='SIZE', action='store', dest='min_size', nargs=1, type=str,
                           help='Min file size threshold. Files smaller than SIZE will be ignored. '
                                'Supported format <VAL><UNIT> where val is positive integer, and '
                                'unit is one letter (case insensitive): b for bytes, k for KiB, '
                                'm for MiB, g for GiB and t for TiB. i.e. "1024" = "1024b" = "1k". '
                                'Default value is {}.'.format(Const.FILE_FILTER_SIZE_MIN))
        group.add_argument('-max', '--max',
                           metavar='SIZE', action='store', dest='max_size', nargs=1, type=str,
                           help='Max file size threshold. Files bigger than SIZE will be ignored. '
                                'Supported format <VAL><UNIT> where val is positive integer, and '
                                'unit is one letter (case insensitive): b for bytes, k for KiB, '
                                'm for MiB, g for GiB and t for TiB. i.e. "1024" = "1024b" = "1k". '
                                'Zero means no max size limit. Default value is {}.'.format(
                                 Const.FILE_FILTER_SIZE_MAX))

        return group

    def _add_other_option_group(self, parser: argparse.ArgumentParser) -> argparse._ArgumentGroup:
        group = parser.add_argument_group('Other')
        group.add_argument('-f', '-force', '--force',
                           action='store_true', dest='force',
                           help='Enforces certain operations (depends on operation context).')

        group.add_argument('-v', '-verbose', '--verbose',
                           action='store_true', dest='verbose',
                           help='Enables verbose output.')

        group.add_argument('-version', '--version', action='version',
                           version='{app} v{v}'.format(app=Const.APP_NAME, v=Const.APP_VERSION))

        group = parser.add_argument_group('Developer tools')
        group.add_argument('-debug', '--debug',
                           action='store_true', dest='debug',
                           help='Enables debug output.')
        group.add_argument('-debug-verbose', '--debug-verbose',
                           action='store_true', dest='debug_verbose',
                           help='Enables verbose debug output (implies --debug).')

        return group

    def _debug_check(self, args: argparse.Namespace) -> None:
        import os

        if args.debug and os.getenv('PYTHONDONTWRITEBYTECODE') is None:
            from .log import Log
            Log.e([
                'Creation of *.pyc files is enabled in your current environment.',
                'This affects Log.d() calls and may produce invalid stacktrace,',
                'and incorrect file and line number shown during runtime.',

                'To disable this, set env variable:',
                '   export PYTHONDONTWRITEBYTECODE=1',
            ])
