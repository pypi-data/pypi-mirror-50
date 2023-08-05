# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""

import json
import os
import sqlite3
from typing import IO

from dhunter.config import Config
from dhunter.const import Const
from dhunter.file_hash import FileHash
from dhunter.file_hash_cache import FileHashCache
from dhunter.hash_base import HashBase
from dhunter.overrides_decorator import overrides


class DirHash(HashBase):

    def __init__(self, path: str, config: Config, load_cache_file: bool = True) -> None:
        self.path: str = path

        self._file_hash_cache: FileHashCache = FileHashCache(path, config)

        if load_cache_file:
            self._file_hash_cache.load()

        from dhunter.hash_manager import HashManager
        self._hash_manager: HashManager = HashManager.get_instance()

        self._config: Config or None = config

    # ------------------------------------------------------------------------------------------------------------

    @property
    @overrides(HashBase)
    def data_type(self) -> str:
        return Const.KEY_FILE_HASH_CACHE

    @property
    @overrides(HashBase)
    def data_version(self) -> int:
        return 1

    @property
    def hash_manager(self):
        if self._hash_manager is None:
            from dhunter.hash_manager import HashManager
            self._hash_manager = HashManager.get_instance()

        return self._hash_manager

    # ------------------------------------------------------------------------------------------------------------

    @property
    def file_count(self) -> int:
        """Returns number of files stored in cache

        :return: number of files stored in cache
        """
        return len(self._file_hash_cache)

    @property
    def total_file_size(self) -> int:
        """Returns total file size of all cached files

        :return: total file size of all cached files
        """
        return self._file_hash_cache.total_file_size

    @total_file_size.setter
    def total_file_size(self, val: int):
        self._file_hash_cache.total_file_size = val

    @property
    def cache(self) -> FileHashCache:
        return self._file_hash_cache

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, val: str) -> None:
        if val != '' and val[-1:] == '/':
            val = val[:-1]
        self._path = val

    # ------------------------------------------------------------------------------------------------------------

    def scan_dir(self) -> None:
        from dhunter.log import Log

        if not os.path.isdir(self.path):
            raise NotADirectoryError('"{path}" is not a directory path.'.format(path=self.path))

        Log.v('{path}/'.format(path=self.path))

        dirs = []
        files = []

        # let's flat-scan the directory and split objects of interest into separate lists
        # NOTE: using sorted() on scandir() kills it slightly, yet this is the only way
        # to show any progress feedack that would be useful to the user.
        for dir_entry in sorted(os.scandir(self.path), key=lambda e: e.name.lower()):
            if not os.path.exists(dir_entry.path):
                Log.vv('{path}: Not found. Skipping.'.format(path=dir_entry.path))
                continue

            if os.path.islink(dir_entry.path):
                Log.vv('{path}: It is the symbolic link. Skipping.'.format(path=dir_entry.path))
                continue

            if self._config.filter.validate_dir(dir_entry.path):
                dirs.append(dir_entry)
                continue

            if self._config.filter.validate_file(dir_entry):
                files.append(dir_entry)
                continue

        # as we use recurrence here, we first hash all the files in the directory, save hash cache for that folder
        # and then dive into subdirectory. That way it's safe to abort almost any time and potentially only hashes
        # of files in currently working folder are lost. But that's ok as all the other data is safe, so we won't
        # be re-hashing anything if not needed.
        if files:
            # keep copy of currently cached file names
            current_cached_names = self._file_hash_cache.keys()

            # add all the files (with hashing if needed)
            # dir_entry is os.DirEntry
            for dir_entry in files:
                # let's build FileHash object (w/o actually hashing file data)
                file_hash = FileHash(dir_entry, self._config, no_hash_calc=True)

                # do we have such file (by name) cached?
                if dir_entry.name not in self._file_hash_cache:
                    # no, add the entry and hash file
                    self._file_hash_cache.add(file_hash)
                else:
                    # check if we match by obj hash, not just by name
                    current_file_hash = self._file_hash_cache.get(dir_entry.name)
                    if file_hash == current_file_hash:
                        # we do, so this is the same, unaltered file, so no need to further check it
                        current_cached_names.remove(file_hash.name)
                        continue

                    # we do not match by obj hash, so most likely this is different data with the same name
                    # we need to update the cache, then remove the name from temp array. We do not need to
                    # check that file as it is updated already
                    self._file_hash_cache.replace(file_hash)
                    current_cached_names.remove(file_hash.name)

            # we have some names left untouched from last cache read. Most likely these files no longer exist
            for file_name in current_cached_names:
                Log.level_push(file_name)
                if not (os.path.exists(file_name) and os.path.isfile(file_name)):
                    self._file_hash_cache.remove(file_name)
                else:
                    Log.e('Zombie file detected: "{name}"'.format(name=file_name))
                Log.level_pop()

            # save directory cache into file and DB
            self.save_cache()

        # now process all the directories
        from dhunter.hash_manager import HashManager
        HashManager.get_instance().scan_dirs(dirs)

    # ------------------------------------------------------------------------------------------------------------

    @overrides(HashBase)
    def to_json(self) -> str:
        attrs = self._get_base_attrs()
        attrs[Const.FIELD_COUNT] = len(self._file_hash_cache)
        attrs['path'] = self.path
        attrs['total_file_size'] = self.total_file_size

        return json.dumps(attrs, separators=(',', ':'))

    def from_json(self, json_string) -> None:
        """Populates instance of FileHash with data from JSON object string

        :param str json_string:
        """
        self.__dict__ = json.loads(json_string)
        self._file_hash_cache = FileHashCache(self.path, self._config)

    # ------------------------------------------------------------------------------------------------------------

    def save_cache(self):
        self._file_hash_cache.save()
        self._hash_manager.insert(self)

    def save_to_fh(self, fh: IO) -> bool:
        fh.write('{json}\n'.format(json=self.to_json()))

        for name, file_hash in self._file_hash_cache.items():
            fh.write(file_hash.to_json())
            fh.write('\n')

        return True

    # ------------------------------------------------------------------------------------------------------------

    def from_db(self, list_of_tuples: sqlite3.Row) -> 'DirHash':
        for item in list_of_tuples:
            self.cache.add(FileHash(item, self._config))

        return self
