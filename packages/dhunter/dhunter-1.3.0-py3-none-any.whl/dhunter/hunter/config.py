# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import os
from argparse import Namespace

from ..core.config_base import ConfigBase
from ..core.const import Const
from ..util.overrides_decorator import overrides


class Config(ConfigBase):

    @staticmethod
    @overrides(ConfigBase)
    def from_args(args: Namespace) -> 'Config':
        from ..core.log import Log
        from ..util.util import Util

        config = Config()

        _keys = [
            # 'duplicates',
            # 'cmd_stats',
            'db_file',
            'sort_by',
            'reverse_order',
            'limit',
            'min_size',
            'max_size',
            # 'force_rehash',
            'verbose',
            'debug',
            'debug_verbose',
            'command',
        ]
        for key in _keys:
            config.__setattr__(key, getattr(args, key))

        if config.limit is not None:
            # noinspection PyUnresolvedReferences
            limit = int(config.limit[0])
            if limit < 0:
                Log.abort('--limit value must be zero or positive integer. "{val}" given'.format(val=limit))
        else:
            limit = 10
        config.limit = limit

        # noinspection PyUnresolvedReferences
        config.min_size = 0 if config.min_size is None else Util.size_to_int(str(config.min_size[0]))
        # noinspection PyUnresolvedReferences
        config.max_size = 0 if config.max_size is None else Util.size_to_int(str(config.max_size[0]))

        config.db_file = None if config.db_file is None else config.db_file[0]
        if not os.path.exists(config.db_file):
            Log.abort('Database file not found.')

        # Let's check if all paths to scan are in fact valid and existing folders
        for single_dir in config.src_dirs:
            if not os.path.exists(single_dir):
                Log.abort('Folder "{dir}" does not exists'.format(dir=single_dir))
            elif not os.path.isdir(os.path.abspath(single_dir)):
                Log.abort('Path "{dir}" is not a folder'.format(dir=single_dir))

        if config.command is None:
            config.command = Const.CMD_DIR_HUNT
        else:
            config.command = config.command[0]
            if config.command not in Const.HUNDER_CMDS:
                Log.abort('Unknown command: "{name}"'.format(name=config.command))

        if config.sort_by is None:
            config.sort_by = 'size'
        else:
            config.sort_by = config.sort_by[0]
            if config.sort_by not in Const.ALLOWED_SORT_VALUES:
                Log.abort('Unknown sort order: "{name}"'.format(name=config.sort_by))

        # after that point, data in Config should be sanitized, validated, usable and useful

        from ..core.filter import Filter
        config.filter = Filter(config)

        return config
