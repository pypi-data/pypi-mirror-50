# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import os
import re
from typing import List

from .config_base import ConfigBase
from .const import Const


class Filter(object):
    _BASE_FILE_NAME_BLACKLIST: List[str] = [
        Const.FILE_DOT_DHUNTER,
        Const.FILE_DOT_IGNORE,
        r'\.env',
        r'\.htaccess',
        r'\.htpasswd',
        r'\.gitignore',
    ]

    _BASE_DIR_NAME_BLACKLIST: List[str] = [
        r'^.*/\.git$',
        r'^.*/\.svn$',
        r'^.*/\.cvs$',
        r'^.*/vendor$',
    ]

    def __init__(self, config: ConfigBase):
        self._file_name_blacklist = Filter._BASE_FILE_NAME_BLACKLIST
        if hasattr(config, 'exclude_file_regexps'):
            self._append_regexp(self._file_name_blacklist, config.exclude_file_regexps)

        self._dir_name_blacklist = Filter._BASE_DIR_NAME_BLACKLIST
        if hasattr(config, 'exclude_dir_regexps'):
            self._append_regexp(self._dir_name_blacklist, config.exclude_dir_regexps)

        self.min_size = config.min_size
        self.max_size = config.max_size

    def _append_regexp(self, to: List[str], regexps: List[str] or None):
        """Appends new regexp rules to existing blacklists."""
        if regexps:
            try:
                for pattern in regexps:
                    re.compile(pattern)
                    if pattern not in to:
                        to.append(pattern)
            except re.error:
                from .log import Log
                # noinspection PyUnboundLocalVariable
                Log.abort('Invalid pattern: {}'.format(pattern))

    # ------------------------------------------------------------------------------------------------------------

    @property
    def min_size(self) -> int:
        return self._min_size

    @min_size.setter
    def min_size(self, val: int):
        self._min_size = val

    @property
    def max_size(self) -> int:
        return self._max_size

    @max_size.setter
    def max_size(self, val: int):
        self._max_size = val

    def validate_file(self, dir_entry: os.DirEntry) -> bool:
        """Validates given DirEntry. Returns False if entry should be completely ignored,
        or True if we want to keep it for further processing.

        Ignore all zero length files. There are usually there for a purpose like .dummy etc,
        so there can be tons of it with the same name even, so by default, ignore them completely.
        Also ignore all symlinks."""

        from .log import Log

        if dir_entry.is_symlink():
            Log.vv('{name}: It is the symbolic link. Skipping.'.format(name=dir_entry.name))
            return False

        # NOTE: do not call is_file() on DirEntry. It will fail in endless
        # recursion for invalid (dead) symbolic links. os.path.isfile() works).
        if not dir_entry.is_file():
            Log.vv('{name}: This is not a file. Skipping.'.format(name=dir_entry.name))
            return False

        item_size = dir_entry.stat().st_size

        if item_size == 0:
            Log.vv('{name}: File is 0 bytes long. Skipping.'.format(name=dir_entry.name))
            return False

        if self.min_size > 0 and item_size < self.min_size:
            Log.vv('{name}: File is shorter than min size ({size}). Skipping.'.format(name=dir_entry.name,
                                                                                      size=item_size))
            return False

        if 0 < self.max_size < item_size:
            Log.vv('{name}: File is biger than max size ({size}). Skipping.'.format(name=dir_entry.name,
                                                                                    size=item_size))
            return False

        for list_item in self._file_name_blacklist:
            match = re.match(list_item, dir_entry.name)
            if match is not None:
                Log.vv('File "{name}" blacklisted by "{re}" rule. Skipping.'.format(name=dir_entry.name, re=list_item))
                return False

        return True

    def validate_dir(self, path: str, no_log: bool = False, warn_on_symlink=False) -> bool:
        """Validates given path. Returns False if entry should be completely ignored,
        or True if keep it for further processing."""

        from .log import Log

        if os.path.islink(path):
            msg = '{path} is a symbolic link. Skipping.'.format(path=path)
            if warn_on_symlink:
                Log.w(msg, not no_log)
            else:
                Log.vv(msg, not no_log)
            return False

        if not os.path.isdir(path):
            Log.vv('{path} is not a directory. Skipping.'.format(path=path), not no_log)
            return False

        for list_item in self._dir_name_blacklist:
            match = re.match(list_item, path)
            if match is not None:
                Log.vv('{path} is blacklisted by "{re}" rule. Skipping.'.format(path=path, re=list_item), not no_log)
                return False

        # if there's dot ignore file present in the folder we completely skip.
        ignore_dot_file = os.path.join(path, Const.FILE_DOT_IGNORE)
        if os.path.exists(ignore_dot_file) and os.path.isfile(ignore_dot_file):
            Log.vv('{name}: Found {dotfile} file in. Skipping.'.format(name=path, dotfile=Const.FILE_DOT_IGNORE),
                   not no_log)
            return False

        return True
