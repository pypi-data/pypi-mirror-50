# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import os
import sqlite3
import typing

from .config_base import ConfigBase
from .dir_hash import DirHash


class HashManager(object):
    _instance: 'HashManager' or None = None

    @staticmethod
    def get_instance(db_file_name: str or None = None, config: ConfigBase or None = None) -> 'HashManager':
        if HashManager._instance is None:
            HashManager._instance = HashManager(db_file_name, config)
        return HashManager._instance

    def __init__(self, db_file_name, config: ConfigBase):
        self.db = None
        self._use_db = db_file_name is not None
        self._db_file_name = db_file_name
        self.config = config

    def __del__(self) -> None:
        self.db_cleanup()

    @property
    def config(self) -> ConfigBase:
        return self._config

    @config.setter
    def config(self, val: ConfigBase):
        self._config = val

    @property
    def db(self) -> sqlite3.Connection:
        return self._db

    @db.setter
    def db(self, val: sqlite3.Connection or None) -> None:
        self._db = val

    # ------------------------------------------------------------------------------------------------------------

    def set_db_dirty(self):
        pass

    def clear_db_dirty(self):
        pass

    # ------------------------------------------------------------------------------------------------------------

    def get_dirhash_for_path(self, dir_path: str) -> DirHash:
        """Creates (or returns existing) DirHash object for given path.
        :param dir_path: Path to get the DirHash for
        """
        dh = DirHash(dir_path, self.config)

        if self._use_db:
            self.db_init()
            cursor = self._db.cursor()
            cursor.execute('SELECT * FROM `files` where `path` = ?', (dir_path,))
            dh.from_db(cursor.fetchall())

        return dh

    def has_dirhash_for_path(self, dir_path: str) -> bool:
        """Checks if we already have dirhash object in project file.

        :param dir_path: Path to look DirHash object for
        """
        result = False

        if self._use_db:
            self.db_init()
            cursor: sqlite3.Cursor = self._db.cursor()
            cursor.execute('SELECT COUNT(`path`) AS `cnt` FROM `files` where `path` = ? LIMIT 1', (dir_path,))
            if cursor.rowcount() == 1 and cursor.fetchone()[0] >= 1:
                result = True

        return result

    def scan_dirs(self, dirs: typing.List[os.DirEntry]) -> None:
        if dirs:
            # set DB dirty so we can detect if user aborted in mid-scanning
            self.set_db_dirty()

            for dir_entry in dirs:
                path = dir_entry.path

                if not os.path.isdir(path):
                    raise NotADirectoryError('"{path}" is not a directory path.'.format(path=path))

                # get the DirHash container for that file folder path
                dir_hash = self.get_dirhash_for_path(path)
                dir_hash.scan_dir()
                dir_hash.save_cache()

            # clear dirty bit
            self.clear_db_dirty()

    # ------------------------------------------------------------------------------------------------------------

    def db_init(self) -> None:
        if self._use_db:
            self._db_connect()
            self._db_create_tables()

    def db_cleanup(self) -> None:
        self.__db_disconnect()

    def _db_connect(self) -> None:
        if self._use_db is False:
            return

        if self._db is None:
            self._db = sqlite3.connect(self._db_file_name)

            self._db.isolation_level = 'EXCLUSIVE'
            self._db.execute('BEGIN EXCLUSIVE')

            self._db.row_factory = sqlite3.Row

    def __db_disconnect(self) -> None:
        if self._db is not None:
            self._db.commit()

            self._db.close()
            self._db = None

    def _db_create_tables(self) -> None:
        if self._use_db is False:
            return

        create_state_table_query = """
        CREATE TABLE IF NOT EXISTS `state` (
            `dirty` INT NOT NULL DEFAULT 0
            );"""

        create_dirs_table_query = """
        CREATE TABLE IF NOT EXISTS `dirs` (
            `path` text NOT NULL DEFAULT ''
            );"""

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
            create_state_table_query,
            'CREATE INDEX IF NOT EXISTS `dirty` ON `state` (`dirty`);',

            create_files_table_query,
            'CREATE INDEX IF NOT EXISTS `path` ON `files` (`path`, `name`);',
            'CREATE INDEX IF NOT EXISTS `hash` ON `files` (`hash`);',

            create_dirs_table_query,
            'CREATE INDEX IF NOT EXISTS `path` ON `dirs` (`path`);',
        ]

        self._db_connect()
        _ = [self._db.cursor().execute(query) for query in queries]

    def insert(self, dir_hash: DirHash or None) -> None:
        if self._use_db is False:
            return

        from .log import Log

        Log.d('insert dir_hash({})'.format(dir_hash.path))

        if dir_hash is None or not isinstance(dir_hash, DirHash):
            raise ValueError('Expecting FileHash instance, received {type}'.format(type=type(dir_hash)))

        self.db_init()

        # delete all old entries for that path
        sql = 'DELETE FROM `files` where `path`=?'
        cur = self._db.cursor()
        cur.execute(sql, (dir_hash.path,))
        self._db.commit()

        if cur.rowcount > 0 and Log.is_debug():
            Log.dd('Deleted {cnt} old entries for {path}'.format(cnt=cur.rowcount, path=dir_hash.path))

        from .const import Const
        for _, file_hash in dir_hash.cache.items():
            if file_hash.name not in [Const.FILE_DOT_IGNORE, Const.FILE_DOT_DHUNTER]:
                file_hash.replace()
        self._db.commit()

    def get_stats(self) -> (int, int, int):
        if not self._use_db:
            return None, None, None

        self.db_init()
        cur = self._db.cursor()

        sql = 'SELECT COUNT(DISTINCT `path`) AS `cnt` FROM `files`'
        cur.execute(sql)
        total_dir_cnt = cur.fetchone()['cnt']

        sql = 'SELECT COUNT(`path`) AS `cnt` FROM `files`'
        cur.execute(sql)
        total_file_cnt = cur.fetchone()['cnt']

        sql = 'SELECT SUM(`size`) AS `size` FROM `files`'
        cur.execute(sql)
        row = cur.fetchone()
        total_file_size = row['size'] if row['size'] is not None else 0

        return total_dir_cnt, total_file_cnt, total_file_size

    def get_hashes_by_count_threshold(self, min_count: int = 1, limit: int or None = None, sort_by: str or None = None,
                                      sort_desc: bool = False) -> (str, str, str, int, float, float, int):
        if not self._use_db:
            raise RuntimeError('No database in use')

        sql = ' SELECT `hash` FROM `files` GROUP BY `hash` HAVING COUNT(`hash`) >= ? '

        if sort_by is not None:
            if sort_by in ['s', 'size']:
                sql += ' ORDER BY `size` '
            elif sort_by in ['c', 'count']:
                sql += ' ORDER BY COUNT(`hash`) '
            else:
                raise RuntimeError('Unknown sorting type: %r' % sort_by)

            sql += ' ASC ' if sort_desc else ' DESC '

        if limit is not None and limit > 0:
            sql += ' LIMIT {}'.format(limit)

        sql += ';'

        self.db_init()

        # we do not want any tuples here, just plain list
        old_row_factory = self._db.row_factory
        self._db.row_factory = lambda cursor, row: row[0]

        c = self._db.cursor()
        c.execute(sql, (min_count,))
        self._db.row_factory = old_row_factory
        return c.fetchall()
