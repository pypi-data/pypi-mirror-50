# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
from typing import List


class Const(object):
    APP_NAME: str = 'dhunter'
    APP_URL: str = 'https://github.com/MarcinOrlowski/dhunter'
    APP_VERSION: str = '0.0.4'

    FIELD_TYPE: str = '_type'
    FIELD_VERSION: str = '_version'
    FIELD_COUNT: int = '_count'

    KEY_HASH_MANAGER: str = 'hm'
    KEY_FILE_HASH: str = 'fh'
    KEY_DIR_HASH: str = 'dh'
    KEY_FILE_HASH_CACHE: str = 'fhc'

    FILE_DOT_DEDUPER: str = '.dhunter'
    FILE_DOT_IGNORE: str = '.dhunterignore'

    ALLOWED_SORT_VALUES: List[str] = [
        's',
        'size',
        'c',
        'count',
    ]
