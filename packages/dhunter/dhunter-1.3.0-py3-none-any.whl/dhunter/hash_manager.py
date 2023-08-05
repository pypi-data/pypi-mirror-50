# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
import os
import sqlite3
import typing

from dhunter.config import Config
from dhunter.dir_hash import DirHash


class HashManager(object):
    __instance: 'HashManager' or None = None

    @staticmethod
    def get_instance(db_file_name: str or None = None, config: Config or None = None) -> 'HashManager':
        if db_file_name is None and HashManager.__instance is None:
            raise RuntimeError('HashManager singleton is not initialized. db_file_name must be given.')
        if HashManager.__instance is None:
            HashManager.__instance = HashManager(db_file_name, config)
        return HashManager.__instance

    def __init__(self, db_file_name, config: Config):
        self.db = None
        if db_file_name is None:
            raise ValueError('Missing DB file name')
        self._db_file_name = db_file_name
        self.config = config

    def __del__(self) -> None:
        self.db_cleanup()

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, val: Config):
        self._config = val

    @property
    def db(self) -> sqlite3.Connection:
        return self.__db

    @db.setter
    def db(self, val: sqlite3.Connection or None) -> None:
        self.__db = val

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

        self.db_init()
        cursor = self.__db.cursor()
        cursor.execute('SELECT * FROM `files` where `path` = ?', (dir_path,))
        return DirHash(dir_path, self.config).from_db(cursor.fetchall())

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
        self.__db_connect()
        self.__db_create_tables()

    def db_cleanup(self) -> None:
        self.__db_disconnect()

    def __db_connect(self) -> None:
        if self.__db is None:
            self.__db = sqlite3.connect(self._db_file_name)

            self.__db.isolation_level = 'EXCLUSIVE'
            self.__db.execute('BEGIN EXCLUSIVE')

            self.__db.row_factory = sqlite3.Row

    def __db_disconnect(self) -> None:
        if self.__db is not None:
            self.__db.commit()

            self.__db.close()
            self.__db = None

    def __db_create_tables(self) -> None:
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

        self.__db_connect()
        _ = [self.__db.cursor().execute(query) for query in queries]

    def __replace_file_hash(self, file_hash) -> None:
        from dhunter.file_hash import FileHash
        from dhunter.log import Log

        Log.level_push()
        Log.dd('insert file hash({})'.format(file_hash.name))

        if file_hash is None or not isinstance(file_hash, FileHash):
            raise ValueError('Expecting FileHash instance, received {type}'.format(type=type(file_hash)))

        self.db_init()

        sql = 'REPLACE INTO files(`path`,`name`,`hash`,`size`,`mtime`,`ctime`,`inode`) VALUES(?,?,?,?,?,?,?)'
        dir_path = os.path.dirname(file_hash.path)
        vals = (dir_path, file_hash.name, file_hash.hash, file_hash.size, file_hash.mtime,
                file_hash.ctime, file_hash.inode)
        cur = self.__db.cursor()
        cur.execute(sql, vals)

        Log.level_pop()

    def insert(self, dir_hash) -> None:
        from dhunter.dir_hash import DirHash
        from dhunter.log import Log

        Log.d('insert dir_hash({})'.format(dir_hash.path))

        if dir_hash is None or not isinstance(dir_hash, DirHash):
            raise ValueError('Expecting FileHash instance, received {type}'.format(type=type(dir_hash)))

        self.db_init()

        # delete all old entries for that path
        sql = 'DELETE FROM `files` where `path`=?'
        cur = self.__db.cursor()
        cur.execute(sql, (dir_hash.path,))
        self.__db.commit()

        if cur.rowcount > 0 and Log.is_debug():
            Log.dd('Deleted {cnt} old entries for {path}'.format(cnt=cur.rowcount, path=dir_hash.path))

        from dhunter.const import Const
        for _, file_hash in dir_hash.cache.items():
            if file_hash.name not in [Const.FILE_DOT_IGNORE, Const.FILE_DOT_DEDUPER]:
                self.__replace_file_hash(file_hash)
        self.__db.commit()

    def get_stats(self) -> (int, int, int):
        self.db_init()
        cur = self.__db.cursor()

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
        sql = ' SELECT `hash` FROM `files` GROUP BY `hash` HAVING COUNT(`hash`) >= ? '

        if sort_by is not None:
            if sort_by in ['s', 'size']:
                sql += ' ORDER BY `size` '
            elif sort_by in ['c', 'count']:
                sql += ' ORDER BY COUNT(`hash`) '
            else:
                raise RuntimeError('Unknown sorting type: %r' % sort_by)

            if sort_desc:
                sql += ' DESC '

        if limit is not None and limit > 0:
            sql += ' LIMIT {}'.format(limit)

        sql += ';'

        self.db_init()

        # we do not want any tuples here, just plain list
        old_row_factory = self.__db.row_factory
        self.__db.row_factory = lambda cursor, row: row[0]

        c = self.__db.cursor()
        c.execute(sql, (min_count,))
        self.__db.row_factory = old_row_factory
        return c.fetchall()
