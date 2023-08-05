# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import datetime
import os
import tempfile

from .args import Args
from .config import Config
from ..core.config_base import ConfigBase
from ..core.const import Const
from ..core.hash_manager import HashManager
from ..core.log import Log
from ..util.util import Util


# noinspection PyMethodMayBeStatic
class Hunter(object):
    _instance: 'Hunter' or None = None

    def __init__(self):
        self.config: ConfigBase or None = None

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_instance() -> 'Hunter':
        if Hunter._instance is None:
            Hunter._instance = Hunter()
        return Hunter._instance

    # ------------------------------------------------------------------------------------------------------------

    @property
    def config(self) -> ConfigBase:
        return self._config

    @config.setter
    def config(self, val: ConfigBase) -> None:
        self._config = val

    # ------------------------------------------------------------------------------------------------------------

    def generate_db_file_name(self) -> str:
        idx = None
        while True:
            suffix = '' if idx is None else '_{idx}'.format(idx=idx)
            db_file = os.path.join(tempfile.gettempdir(), '{app}_{stamp}{suffix}.sqlite'.format(
                app=Const.APP_NAME, stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), suffix=suffix))
            if not os.path.exists(db_file):
                break

            idx += 1
            continue

        return db_file

    # ------------------------------------------------------------------------------------------------------------

    def show_stats(self) -> None:
        hm = HashManager.get_instance()

        dir_cnt, file_cnt, total_file_size = hm.get_stats()
        Log.banner([
            'Dirs : {}'.format(dir_cnt),
            'Files: {}'.format(file_cnt),
            'Size : {}'.format(Util.size_to_str(total_file_size))
        ])

    # ------------------------------------------------------------------------------------------------------------

    # noinspection PyUnusedLocal
    def clean_db(self, config: ConfigBase) -> None:
        dead_rowids = []

        hm = HashManager.get_instance()
        hm.db_init()

        cursor = hm.db.cursor()
        query = 'SELECT ROWID, * FROM `files` ORDER BY ROWID'
        cursor.execute(query)

        Log.level_push('Looking for dead entries')
        for row in cursor:
            full_path = os.path.join(row['path'], row['name'])

            # check if this file still exists and update DB if not
            if not os.path.exists(full_path):
                Log.e('{path}'.format(path=full_path), prefix='')
                dead_rowids.append(row['ROWID'])

        Log.i('Dead entries found: {}'.format(len(dead_rowids)))
        Log.level_pop()

        if dead_rowids:
            Log.level_push('Updating database')
            cursor = hm.db.cursor()
            for row_id in dead_rowids:
                cursor.execute('DELETE FROM `files` WHERE `ROWID`=?', (row_id,))
            Log.level_pop()

    # ------------------------------------------------------------------------------------------------------------

    def show_file_duplicates(self, config: ConfigBase) -> None:
        hm = HashManager.get_instance()

        limit: int = config.limit
        sort_by: str = config.sort_by
        reverse_order: bool = config.reverse_order

        # get all files with non unique hashes (at least 2 counts)
        dupli_hashes = hm.get_hashes_by_count_threshold(2, limit, sort_by, reverse_order)

        if not dupli_hashes:
            Log.i('No duplicated files found.')
            return

        Log.banner('Duplicates')

        stats_duplicates_total_count = 0
        stats_duplicates_bytes_total = 0

        cursor = hm.db.cursor()
        query = 'SELECT ROWID, * FROM `files` WHERE `size` >= ? AND `hash` = ?'
        if config.max_size > 0:
            query += ' AND `size` <= ? '
        query += 'ORDER BY `path`,`name`'
        for file_hash_idx, file_hash in enumerate(dupli_hashes, start=1):
            args = [config.min_size, file_hash]
            if config.max_size > 0:
                args.append(config.max_size)
            cursor.execute(query, tuple(args))

            group_header_shown = False
            dupli_rows = cursor.fetchall()
            for idx, row in enumerate(dupli_rows, start=1):
                if not group_header_shown:
                    duplicate_count = (len(dupli_rows) - 1)
                    total_duplicates_size = duplicate_count * row['size']

                    stats_duplicates_total_count += duplicate_count
                    stats_duplicates_bytes_total += total_duplicates_size

                    Log.level_push('{idx:2d}: size: {size:s}, duplicates: {dupes:d}, wasted: {wasted:s}'.format(
                        idx=file_hash_idx,
                        size=Util.size_to_str(row['size']),
                        dupes=duplicate_count,
                        wasted=Util.size_to_str(total_duplicates_size)))
                    group_header_shown = True

                full_path = os.path.join(row['path'], row['name'])
                log_msg = '{idx:2d}: {path}'.format(idx=idx, path=full_path)

                # check if this file still exists and update DB if not
                if not os.path.exists(full_path):
                    cursor = hm.db.cursor()
                    cursor.execute('DELETE FROM `files` WHERE `ROWID`=?', (row['ROWID'],))
                    Log.e(log_msg, prefix='')
                else:
                    Log.i(log_msg)

            if group_header_shown:
                Log.level_pop()

        Log.i(' ')
        Log.level_push('Summary')
        fmt = '{files_cnt:d} files have {dupes_cnt:d} duplicates, wasting together {size:s}.'
        Log.i(fmt.format(files_cnt=len(dupli_hashes), dupes_cnt=stats_duplicates_total_count,
                         size=Util.size_to_str(stats_duplicates_bytes_total)))
        Log.level_pop()

    # ------------------------------------------------------------------------------------------------------------

    def main(self) -> int:
        rc = 0

        try:
            # parse common line arguments
            args = Args()

            self.config = Config.from_args(args.parse_args())
            Log.configure(self.config)
            Log.disable_buffer()

            # init hash manager singleton
            HashManager.get_instance(self.config.db_file, self.config)

            if self.config.command == Const.CMD_FILE_HUNT:
                self.show_file_duplicates(self.config)
            elif self.config.command == Const.CMD_DIR_HUNT:
                self.show_dir_duplicates(self.config)
            elif self.config.command == Const.CMD_CLEAN_DB:
                self.clean_db(self.config)
            else:
                Log.abort('Unknown command: {cmd}'.format(cmd=self.config.command))

        except (ValueError, IOError) as ex:
            if not self.config.debug:
                raise
            Log.e(str(ex))
            rc = 1

        return rc

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start() -> int:
        """Application entry point.
        """
        Util.validate_env()
        return Hunter().main()
