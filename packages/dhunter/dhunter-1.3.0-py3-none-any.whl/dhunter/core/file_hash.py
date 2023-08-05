# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import json
import os
import sqlite3
from datetime import datetime
from typing import List

from .config_base import ConfigBase
from .const import Const
from .db_base import DbBase
from .hash_base import HashBase
from ..util.overrides_decorator import overrides
from ..util.util import Util


# noinspection PyAbstractClass
class FileHash(HashBase, DbBase):

    # ------------------------------------------------------------------------------------------------------------

    @property
    @overrides(HashBase)
    def data_type(self) -> str:
        return Const.KEY_FILE_HASH

    @property
    @overrides(HashBase)
    def data_version(self) -> int:
        return 1

    # -----------------------------------------------------------------------------------------------------------

    def __init__(self, arg: os.DirEntry or str or sqlite3.Row or None, config: ConfigBase,
                 file_hash: str or None = None, dir_path: str or None = None, no_hash_calc: bool = False) -> None:

        super().__init__(config.db_file)

        self.hash = file_hash
        self.hash_time_seconds = 0
        self.name = None
        self.size = 0
        self.mtime = 0
        self.ctime = 0
        self.inode = 0

        self.path = None

        if arg is not None:
            if isinstance(arg, os.DirEntry):
                self.from_dir_entry(arg, file_hash, no_hash_calc)
            elif isinstance(arg, sqlite3.Row):
                self.hash = arg['hash']
                self.path = arg['path']
                self.name = arg['name']
                self.size = arg['size']
                self.mtime = arg['mtime']
                self.ctime = arg['ctime']
                self.inode = arg['inode']

            elif isinstance(arg, str):
                self.from_json(arg)
                if dir_path is not None and self.name is not None:
                    self.path = os.path.join(dir_path, self.name)
            else:
                raise ValueError('Unsupported data type {type}'.format(type=type(arg)))

    # TODO: ensure inodes on filesystems with Copy-On-Write are not the same for all the duplicates

    def __key(self) -> (str, int, datetime, datetime, int):
        return self.name_hash, self.inode, self.ctime, self.mtime, self.size

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        return isinstance(self, type(other)) and self.__key() == other.__key()

    # -----------------------------------------------------------------------------------------------------------

    def from_dir_entry(self, dir_entry: os.DirEntry, file_hash: str or None = None, dont_hash: bool = False) -> None:
        if not isinstance(dir_entry, os.DirEntry):
            raise ValueError('Unsupported data type {type}'.format(type=type(dir_entry)))

        self.hash = file_hash
        self.name = dir_entry.name
        self.path = dir_entry.path
        self.size = dir_entry.stat().st_size
        self.ctime = self._strip_millis(dir_entry.stat().st_ctime)
        self.mtime = self._strip_millis(dir_entry.stat().st_mtime)
        self.inode = dir_entry.stat().st_ino

        if not dont_hash:
            self.calculate_hash()

    # -----------------------------------------------------------------------------------------------------------

    def _strip_millis(self, stamp) -> int:
        stamp = str(stamp)
        if stamp.find('.') >= 0:
            stamp = stamp.split('.')[0]

        return int(stamp)

    @property
    def name(self) -> str or None:
        return self._name

    @name.setter
    def name(self, val: str) -> None:
        self._name = val
        self._name_hash = val if val is None else Util.md5(val)

    @property
    def name_hash(self) -> str or None:
        return self._name_hash

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, val: int) -> None:
        self._size = val

    @property
    def mtime(self) -> int:
        return self._mtime

    @mtime.setter
    def mtime(self, val: int) -> None:
        self._mtime = val

    @property
    def ctime(self) -> int:
        return self._ctime

    @ctime.setter
    def ctime(self, val: int) -> None:
        self._ctime = val

    @property
    def inode(self) -> int:
        return self._inode

    @inode.setter
    def inode(self, val: int) -> None:
        self._inode = val

    @property
    def hash_time_seconds(self) -> int:
        return self._hash_time_seconds

    @hash_time_seconds.setter
    def hash_time_seconds(self, val: int) -> None:
        self._hash_time_seconds = val

    @property
    def hash(self) -> str or None:
        if self._hash is None:
            self.calculate_hash()

        return self._hash

    @hash.setter
    def hash(self, hash_value: str or None) -> None:
        if not (hash_value is None or isinstance(hash_value, str)):
            raise ValueError('String or None expected. {type} provided'.format(type=type(hash_value)))

        if hash_value is None:
            self.hash_time_seconds = 0

        self._hash = hash_value

    # -----------------------------------------------------------------------------------------------------------

    def calculate_hash(self) -> None:
        """Calculates hash for given file of this FileHash object.

        :raises FileNotFoundError
        :raises OSError
        """
        if self.name is None:
            raise OSError('File name cannot be None')
        elif self.path is None:
            raise OSError('File path cannot be None')

        if not os.path.exists(self.path):
            raise FileNotFoundError('"{name}" not found'.format(name=self.path))
        elif not os.path.isfile(self.path):
            raise OSError('"{name}" is not a file'.format(name=self.path))

        dir_name = os.path.dirname(self.path)
        cmd = []
        # if self.size > (1024 * 1024 * 10):
        #     cmd = ['nice', '-n', str(5)]
        cmd.extend(['md5sum', '-b', '--', self.name])
        rc, elapsed_time_seconds, stdout, stderr = Util.execute(cmd, dir_name)

        from .log import Log
        if rc == 0:
            # hash is always plain hex string. No need for utf-8 here, esp. it ends up in JSON files.
            self.hash = stdout[0].decode('utf8').split(' ')[0]
            self.hash_time_seconds = elapsed_time_seconds

            Log.d('{name}: hash {hash} in {sec} secs.'.format(name=self.path, hash=self.hash,
                                                              sec=self.hash_time_seconds))
        else:
            Log.e('Failed to hash "{name}"'.format(name=self.path))

    # -----------------------------------------------------------------------------------------------------------

    def exists(self) -> bool:
        """Checks if file this object refers to, is still present in current folder."""
        return os.path.exists(self.path)

    # -----------------------------------------------------------------------------------------------------------

    _json_keys: List[str] = ['hash', 'name', 'size', 'mtime', 'ctime', 'inode']

    @overrides(HashBase)
    def to_json(self) -> str:
        attrs = self._get_base_attrs()

        for key in self._json_keys:
            attrs[key] = self.__getattribute__(key)

        return json.dumps(attrs, separators=(',', ':'))

    def from_json(self, json_string: str) -> None:
        """Populates instance of FileHash with data from JSON object string.
        """

        tmp = json.loads(json_string)
        for field in self._json_keys:
            self.__setattr__(field, tmp.get(field))

        self.hash_time_seconds = 0

    # -----------------------------------------------------------------------------------------------------------

    @overrides(DbBase)
    def create_tables(self) -> None:
        create_files_table_query = """
        CREATE TABLE IF NOT EXISTS `files` (
            `path` text NOT NULL DEFAULT '',
            `name` text NOT NULL DEFAULT '',
            `hash` text NOT NULL DEFAULT '',
            `size` INT NOT NULL DEFAULT 0,
            `mtime` INT NOT NULL DEFAULT 0,
            `ctime` INT NOT NULL DEFAULT 0,
            `inode` INT NOT NULL DEFAULT 0
            );"""

        queries = [
            create_files_table_query,
            'CREATE INDEX IF NOT EXISTS `path` ON `files` (`path`, `name`);',
            'CREATE INDEX IF NOT EXISTS `hash` ON `files` (`hash`);',
        ]

        self.__create_tables(queries)

    def replace(self) -> None:
        self.__db_connect()

        sql = 'REPLACE INTO files(`path`,`name`,`hash`,`size`,`mtime`,`ctime`,`inode`) VALUES(?,?,?,?,?,?,?)'
        dir_path = os.path.dirname(self.path)
        vals = (dir_path, self.name, self.hash, self.size, self.mtime, self.ctime, self.inode)

        cur = self.__db.cursor()
        cur.execute(sql, vals)
