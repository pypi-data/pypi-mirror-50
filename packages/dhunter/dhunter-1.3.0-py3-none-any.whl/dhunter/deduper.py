# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""

import os

from dhunter.hash_manager import HashManager
from dhunter.log import Log
from dhunter.util import Util


class Deduper(object):

    @staticmethod
    def show_duplicates(limit: int = 0, sort_by: str = 'size', reverse_order: bool = False) -> None:
        hm = HashManager.get_instance()

        # get all files with non unique hashes (at least 2 counts)
        dupli_hashes = hm.get_hashes_by_count_threshold(2, limit, sort_by, reverse_order)

        if not dupli_hashes:
            Log.i('No duplicated files found.')
            return

        Log.banner('Duplicates')

        stats_duplicates_total_count = 0
        stats_duplicates_bytes_total = 0

        cursor = hm.db.cursor()
        query = 'SELECT * FROM `files` WHERE `hash` = ? ORDER BY `path`,`name` '
        for file_hash_idx, file_hash in enumerate(dupli_hashes, start=1):
            cursor.execute(query, (file_hash,))

            group_header_shown = False
            dupli_rows = cursor.fetchall()
            for idx, row in enumerate(dupli_rows, start=1):
                if not group_header_shown:
                    duplicate_count = (len(dupli_rows) - 1)
                    total_duplicates_size = duplicate_count * row['size']

                    stats_duplicates_total_count += duplicate_count
                    stats_duplicates_bytes_total += total_duplicates_size

                    Log.level_push('{idx:2d}: size: {size:s}, duplicates: {dupes:d}, wasted: {wasted:s}'.format(
                            idx=file_hash_idx, size=Util.size_format(row['size']),
                            dupes=duplicate_count, wasted=Util.size_format(total_duplicates_size)),
                    )
                    group_header_shown = True

                Log.i('{idx:2d}: {path}'.format(idx=idx, path=os.path.join(row['path'], row['name'])))

            Log.level_pop()

        Log.level_push('Summary')
        fmt = '{files_cnt:d} files has {dupes_cnt:d} duplicates, wasting {size:s}.'
        Log.i(fmt.format(files_cnt=len(dupli_hashes), dupes_cnt=stats_duplicates_total_count,
                         size=Util.size_format(stats_duplicates_bytes_total)))
        Log.level_pop()

    @staticmethod
    def show_stats() -> None:
        hm = HashManager.get_instance()

        dir_cnt, file_cnt, total_file_size = hm.get_stats()
        Log.banner([
            'Dirs : {}'.format(dir_cnt),
            'Files: {}'.format(file_cnt),
            'Size : {}'.format(Util.size_format(total_file_size))
        ])
