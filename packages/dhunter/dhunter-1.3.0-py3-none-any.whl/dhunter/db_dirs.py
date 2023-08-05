# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""

from dhunter.db_base import DbBase
from dhunter.overrides_decorator import overrides


# noinspection PyAbstractClass
class DbDirs(DbBase):

    @overrides(DbBase)
    def create_tables(self) -> None:
        create_dirs_table_query = """
        CREATE TABLE IF NOT EXISTS `dirs` (
            `path` text NOT NULL DEFAULT '',
            );"""

        queries = [
            create_dirs_table_query,
            'CREATE INDEX IF NOT EXISTS `path` ON `dirs` (`path`);',
        ]

        self.__create_tables(queries)
