# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
import datetime
import os
import sys
import tempfile

from dhunter.args import Args
from dhunter.config import Config
from dhunter.const import Const
from dhunter.deduper import Deduper
from dhunter.hash_manager import HashManager
from dhunter.log import Log
from dhunter.util import Util


# noinspection PyMethodMayBeStatic
class App(object):
    _instance: 'App' or None = None

    def __init__(self):
        self.config: Config or None = None

    # ------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_instance() -> 'App':
        if App._instance is None:
            App._instance = App()
        return App._instance

    # ------------------------------------------------------------------------------------------------------------

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, val: Config) -> None:
        self._config = val

    # ------------------------------------------------------------------------------------------------------------

    def generate_db_file_name(self) -> str:
        idx = None
        while True:
            suffix = '' if idx is None else '_{idx}'.format(idx=idx)
            state_file = os.path.join(tempfile.gettempdir(), '{app}_{stamp}{suffix}.sqlite'.format(
                    app=Const.APP_NAME, stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'), suffix=suffix))
            if not os.path.exists(state_file):
                break

            idx += 1
            continue

        return state_file

    def main(self) -> int:
        rc = 0

        try:
            # parse common line arguments
            self.config = Config.from_args(Args.parse_args())
            Log.configure(self.config)
            Log.disable_buffer()

            if self.config.state_file is None:
                self.config.state_file = self.generate_db_file_name()
                do_folder_scan = True
            else:
                do_folder_scan = not (os.path.exists(self.config.state_file) and os.path.isfile(self.config.state_file))

                if not do_folder_scan and self.config.src_dirs is not None:
                    do_folder_scan = True

            Log.i('Using DB file: "{name}"'.format(name=self.config.state_file))

            start_stamp = datetime.datetime.now()
            Log.banner_v('Started at {stamp}'.format(stamp=start_stamp.replace(microsecond=0)), top=False)

            if do_folder_scan:
                Log.d('Scanning source dirs')
                hm = HashManager.get_instance(self.config.state_file, self.config)
                for path in self.config.src_dirs:
                    if not self.config.filter.validate_dir(path):
                        continue

                    dir_hash = hm.get_dirhash_for_path(path)
                    dir_hash.scan_dir()
            else:
                Log.d('Scan skipped.')

            end_stamp = datetime.datetime.now()
            time_elapsed = end_stamp - start_stamp

            # show some stats
            if Log.is_verbose():
                self.show_stats()
                Log.banner([
                    'Started  : {stamp}'.format(stamp=start_stamp.replace(microsecond=0)),
                    'Completed: {stamp}'.format(stamp=end_stamp.replace(microsecond=0)),
                    'Elapsed  : {elapsed}'.format(elapsed=Util.remove_microseconds(time_elapsed)),
                ], bottom=False, top=False)

            if self.config.duplicates:
                Deduper.show_duplicates(self.config.limit, self.config.sort_by, self.config.reverse_order)
            elif self.config.cmd_stats:
                self.show_stats()

        except (ValueError, IOError) as ex:
            if not self.config.debug:
                Log.e(str(ex))
                rc = 1
            else:
                raise

        return rc

    # application entry point
    @staticmethod
    def cli() -> int:
        required_version = (3, 6)
        current_version = sys.version_info

        if current_version < required_version:
            req_minior, req_major, *_ = required_version
            cur_minior, cur_major, *_ = current_version
            req_v = str(req_minior) + '.' + str(req_major)
            cur_v = str(cur_minior) + '.' + str(cur_major)
            print('Requires Python v{v}+, but you have v{oldv}. '
                  'Please upgrade your Python to at least v{v}.'.format(v=req_v, oldv=cur_v))
            sys.exit(1)

        from dhunter.app import App
        app = App()
        return app.main()
