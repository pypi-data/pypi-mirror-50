# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
import os
from argparse import Namespace
from typing import List

from dhunter.const import Const


class Config(object):

    def __init__(self):
        self.src_dirs: List[str] = []
        self.duplicates: bool = False
        self.cmd_stats: bool = False
        self.state_file: str or None = None
        self.sort_by: str = None
        self.reverse_order: bool = False
        self.limit: int = 0
        self.min_size: int = 0
        self.max_size: int = 0
        self.force_rehash: bool = False
        self.verbose: bool = False
        self.debug: bool = False
        self.debug_verbose: bool = False
        self.filter = None

    @staticmethod
    def from_args(args: Namespace) -> 'Config':
        from dhunter.log import Log
        from dhunter.util import Util

        config = Config()

        _keys = [
            'src_dirs',
            'duplicates',
            'cmd_stats',
            'state_file',
            'sort_by',
            'reverse_order',
            'limit',
            'min_size',
            'max_size',
            'force_rehash',
            'verbose',
            'debug',
            'debug_verbose',
        ]
        for key in _keys:
            config.__setattr__(key, getattr(args, key))

        if config.limit is not None:
            limit = int(config.limit)
            if limit < 0:
                Log.abort('--limit value must be zero or positive integer. "{val}" given'.format(val=limit))
        else:
            limit = 0
        config.limit = limit

        config.min_size = 0 if config.min_size is None else Util.size_to_int(str(config.min_size[0]))
        config.max_size = 0 if config.max_size is None else Util.size_to_int(str(config.max_size[0]))

        config.state_file = None if config.state_file is None else config.state_file[0]
        if config.state_file is None:
            if config.src_dirs is None:
                Log.abort('You must specify at least one folder to scan.')
        else:
            if not os.path.exists(config.state_file) or not os.path.isfile(config.state_file):
                if config.src_dirs is None:
                    Log.abort('State file does not exists. You must specify at least one folder to scan.')

        # Let's check if all paths to scan are in fact valid and existing folders
        for single_dir in config.src_dirs:
            if not os.path.exists(single_dir):
                Log.abort('Folder "{dir}" does not exists'.format(dir=single_dir))
            elif not os.path.isdir(os.path.abspath(single_dir)):
                Log.abort('Path "{dir}" is not a folder'.format(dir=single_dir))

        config.sort_by = config.sort_by
        if config.sort_by is None:
            config.sort_by = 'size'
        else:
            config.sort_by = config.sort_by[0]
            if config.sort_by not in Const.ALLOWED_SORT_VALUES:
                Log.abort('Unknown sort order: "{name}"'.format(name=config.sort_by))

        if config.sort_by is not None:
            config.sort_by = config.sort_by[0]
        else:
            config.sort_by = 'size'

        # after that point, data in Config should be sanitized, validated, usable and useful

        from dhunter.filter import Filter
        config.filter = Filter(config)

        return config
