# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
import json
import os
from typing import Dict, IO, ItemsView, List

from dhunter.config import Config
from dhunter.const import Const
from dhunter.file_hash import FileHash
from dhunter.hash_base import HashBase
from dhunter.overrides_decorator import overrides


class FileHashCache(HashBase):

    # ------------------------------------------------------------------------------------------------------------

    @property
    @overrides(HashBase)
    def data_type(self) -> str:
        return Const.KEY_FILE_HASH

    @property
    @overrides(HashBase)
    def data_version(self) -> int:
        return 1

    # ------------------------------------------------------------------------------------------------------------

    # noinspection PyPep8Naming
    @property
    def FILE_HASH_TIME_THRESHOLD_SECONDS(self) -> int:
        return 3

    # ------------------------------------------------------------------------------------------------------------

    def __init__(self, path: str, config: Config):
        self.__setattr__(Const.FIELD_TYPE, self.data_type)
        self.__setattr__(Const.FIELD_VERSION, self.data_version)

        self._cache: Dict[str, FileHash] = {}
        self._dirty: bool = False
        self._path: str = path
        self._total_file_size: int = 0

        if config is None:
            from dhunter.app import App
            config = App.get_instance().config
        self._config = config

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, item) -> bool:
        return item in self._cache

    def __getitem__(self, path) -> FileHash:
        return self._cache.get(path)

    # ------------------------------------------------------------------------------------------------------------

    def items(self) -> ItemsView[str, FileHash]:
        return self._cache.items()

    # ------------------------------------------------------------------------------------------------------------

    @property
    def total_file_size(self) -> int:
        return self._total_file_size

    @total_file_size.setter
    def total_file_size(self, val: int) -> None:
        self._total_file_size = val

    def get(self, file_name, default_value=None) -> FileHash or None:
        return self._cache.get(file_name, default_value)

    # ------------------------------------------------------------------------------------------------------------

    def keys(self) -> List[str]:
        return list(self._cache.keys())

    # ------------------------------------------------------------------------------------------------------------

    def load(self) -> None:
        """Loads FileHashes from from flat file storage
        """
        if not os.path.isdir(self._path):
            raise NotADirectoryError('"{name}" is not a directory'.format(name=self._path))

        from dhunter.file_hash import FileHash

        # if we are forced to rehash all files, then we pretend
        # there was no file to load...
        if self._config.force_rehash:
            self._dirty = True
            return

        # we need to prevent dirty state as loading should not affect that flag at all
        dirty = self._dirty
        dot_file_name = os.path.join(self._path, Const.FILE_DOT_DEDUPER)

        if os.path.isfile(dot_file_name):
            # is header line read already?
            file_hash_meta_read = False

            with open(dot_file_name, 'r') as file_handle:
                for line in file_handle:
                    line = line.strip('\n').strip()

                    if not line or line[0] == '#':
                        continue

                    if not file_hash_meta_read:
                        # we need to read cache meta data. For now it is not really needed.
                        file_hash_meta_read = True
                        continue

                    filehash = FileHash(line, self._config, dir_path=self._path, no_hash_calc=True)
                    if filehash.exists():
                        self.add(filehash)
                    else:
                        from dhunter.log import Log
                        Log.w('Not found: {}'.format(self._path))

        self._dirty = dirty

    def save(self) -> bool:
        """Saves FileHash hashes into flat file storage
        """
        result = False
        if self._dirty:
            dot_file_name = os.path.join(self._path, Const.FILE_DOT_DEDUPER)

            with open(dot_file_name, 'w') as fh:
                fh.write('# {name} hash cache {url}\n'.format(name=Const.APP_NAME, url=Const.APP_URL))
                self.save_to_fh(fh)
                fh.close()

                result = True

            self._dirty = False

        return result

    def save_to_fh(self, fh: IO, save_if_non_dirty_too: bool = False) -> bool:
        result = False
        can_save = self._dirty

        if not self._dirty and save_if_non_dirty_too:
            can_save = True

        if can_save:
            # 1st row is JSON object with data for DirHash
            fh.write('{json}\n'.format(json=self.to_json()))
            fh.write('\n')

            # all the FileHash objects
            for file_hash in self._cache.values():
                fh.write('{json}\n'.format(json=file_hash.to_json()))

            result = True

        return result

    # @overrides(HashBase)
    # def _get_json_export_attrs(self) -> List[str]:
    #     return [self.data_type_filed_name, self.data_version_field_name]

    # ------------------------------------------------------------------------------------------------------------

    @overrides(HashBase)
    def to_json(self) -> str:
        attrs = self._get_base_attrs()
        attrs[Const.FIELD_COUNT] = len(self._cache)

        return json.dumps(attrs, separators=(',', ':'))

    # ------------------------------------------------------------------------------------------------------------

    def add(self, file_hash: FileHash) -> None:
        """Add FileHash to internal cache storage

        :raises ValueError
        """
        if not isinstance(file_hash, FileHash):
            raise ValueError('Unsupported data type {type}'.format(type=type(file_hash)))

        # check if we have this hash entry in cache already?
        if file_hash not in self._cache.values():
            # no, create new entry then
            self._add_finalize(file_hash)
        elif file_hash.name in self._cache:
            # we do, so let's check if that is for this particular file state
            current_file_hash = self._cache.get(file_hash.name)
            if file_hash != current_file_hash:
                # seems it is not. Most likely underlying data changed,
                # while filename and/or size did not. Need to replace old
                # entry with new one then.

                # in case size changed, we need to keep cached totals up to date
                self._total_file_size -= current_file_hash.size

                # replace old object
                self.replace(file_hash.name)

                # update hash, and totals
                self._add_finalize(file_hash)

    def _add_finalize(self, file_hash: FileHash) -> None:
        # force file data hash calculation if not done yet
        if file_hash.hash is None:
            file_hash.calculate_hash()

        # store new object in cache
        self._cache[file_hash.name] = file_hash

        # update totals
        self._total_file_size += file_hash.size

        # flag cache dirty for saving
        self._dirty = True

        # if calculation of hash took more than FILE_HASH_TIME_THRESHOLD_SECONDS
        # we force cache file save on adding such hashto avoid re-hashing
        if file_hash.hash_time_seconds >= self.FILE_HASH_TIME_THRESHOLD_SECONDS:
            self.save()

    # ------------------------------------------------------------------------------------------------------------

    def replace(self, file_hash: FileHash) -> bool:
        """Replaces existing FileHash entry with new one or just adds new entry if no file_hash is cached yet.
        :returns indicating if FileHash was replaced (True), or just added (False)
        """
        replaced = False
        if file_hash.name in self._cache:
            del self._cache[file_hash.name]
            replaced = True

        self.add(file_hash)

        return replaced

    # ------------------------------------------------------------------------------------------------------------

    def remove(self, obj: os.DirEntry or FileHash or str) -> bool:
        """Removes cached entry based on of either DirEntry or FileHash data. Does nothing if object is not found
        """
        if isinstance(obj, (FileHash, os.DirEntry)):
            return self.remove_by_name(obj.name)
        if isinstance(obj, str):
            return self.remove_by_name(obj)

        raise ValueError('Unsupported argument type "{}"'.format(type(obj)))

    def remove_by_name(self, name: str) -> bool:
        """Removes cached file entry based on file name. Does nothing if object is not found
        """
        result = False
        if name in self._cache:
            del self._cache[name]
            self._dirty = True
            result = True

        return result
