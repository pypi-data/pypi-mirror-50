# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import datetime
import os

from .args import Args
from .config import Config
from ..core.const import Const
from ..core.hash_manager import HashManager
from ..core.log import Log
from ..util.util import Util


# noinspection PyMethodMayBeStatic
class Scanner(object):
    _instance: 'Scanner' or None = None

    def __init__(self):
        self.config: Config or None = None

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_instance() -> 'Scanner':
        if Scanner._instance is None:
            Scanner._instance = Scanner()
        return Scanner._instance

    # ------------------------------------------------------------------------------------------------------------

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, val: Config) -> None:
        self._config = val

    # ------------------------------------------------------------------------------------------------------------

    def show_stats(self) -> None:
        hm = HashManager.get_instance()

        dir_cnt, file_cnt, total_file_size = hm.get_stats()
        if dir_cnt is not None:
            Log.banner([
                'Dirs : {}'.format(dir_cnt),
                'Files: {}'.format(file_cnt),
                'Size : {}'.format(Util.size_to_str(total_file_size))
            ])

    # ------------------------------------------------------------------------------------------------------------

    def _cmd_scan(self):
        # init hash manager singleton
        hm = HashManager.get_instance(self.config.db_file, self.config)

        Log.d('Scanning source dirs')
        for path in self.config.src_dirs:
            if not self.config.filter.validate_dir(path, warn_on_symlink=True):
                continue

            # we need to work on full paths otherwise hash database
            # would be completely useless w/o knowing starting directory
            # or while scanning more than one DIRs
            if not self.config.relative_paths:
                path = os.path.abspath(path)

            dir_hash = hm.get_dirhash_for_path(path)
            dir_hash.scan_dir()

    def _cmd_check(self):
        # init hash manager singleton
        hm = HashManager.get_instance(self.config.db_file, self.config)

        Log.d('Validating source dirs')
        for path in self.config.src_dirs:
            if not self.config.filter.validate_dir(path):
                continue

            result = '        ' if hm.has_dirhash_for_path(path) else 'NOT FOUND'
            print('[{res}]: {path}'.format(res=result, path=path))

    def main(self) -> int:
        rc = 0

        try:
            # parse common line arguments
            args = Args()
            self.config = Config.from_args(args.parse_args())
            Log.configure(self.config)
            Log.disable_buffer()

            start_stamp = datetime.datetime.now()
            Log.banner('Started at {stamp}'.format(stamp=start_stamp.replace(microsecond=0)), top=False)

            cmds = {
                Const.CMD_SCAN: self._cmd_scan,
                Const.CMD_CHECK: self._cmd_check,
            }
            if self.config.command in cmds:
                cmds[self.config.command]()

            end_stamp = datetime.datetime.now()
            time_elapsed = end_stamp - start_stamp

            # show some stats
            self.show_stats()

            Log.banner('Scan time: {elapsed}'.format(elapsed=Util.remove_microseconds(time_elapsed)),
                       bottom=False, top=False)

        except (ValueError, IOError) as ex:
            if self.config.debug:
                raise
            Log.e(str(ex))
            rc = 1

        return rc

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start() -> int:
        """Application scanner entry point.
        """
        Util.validate_env()
        return Scanner().main()
