# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

from typing import List


class Const(object):
    APP_NAME: str = 'dhunter'
    APP_URL: str = 'https://github.com/MarcinOrlowski/dhunter'
    APP_VERSION: str = '1.3.0'

    FIELD_TYPE: str = '_type'
    FIELD_VERSION: str = '_version'
    FIELD_COUNT: int = '_count'

    KEY_HASH_MANAGER: str = 'hm'
    KEY_FILE_HASH: str = 'fh'
    KEY_DIR_HASH: str = 'dh'
    KEY_FILE_HASH_CACHE: str = 'fhc'

    FILE_DOT_DHUNTER: str = '.dhunter'
    FILE_DOT_IGNORE: str = '.dhunterignore'

    FILE_FILTER_SIZE_MIN = 2048
    FILE_FILTER_SIZE_MAX = 0

    ALLOWED_SORT_VALUES: List[str] = [
        's',
        'size',
        'c',
        'count',
    ]

    CMD_SCAN = 'scan'
    CMD_CHECK = 'check'

    SCANNER_CMDS = [
        CMD_SCAN,
        CMD_CHECK,
    ]

    CMD_FILE_HUNT = 'filehunt'
    CMD_DIR_HUNT = 'dirhunt'
    CMD_CLEAN_DB = 'cleandb'
    HUNDER_CMDS = [
        CMD_FILE_HUNT,
        # CMD_DIR_HUNT,
        CMD_CLEAN_DB,
    ]
