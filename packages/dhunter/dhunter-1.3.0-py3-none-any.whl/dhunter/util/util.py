# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""

import os
import time
from datetime import timedelta
from typing import List

from ..core.const import Const
from ..core.log import Log


class Util(object):
    @staticmethod
    def execute(cmd_list: List[str], working_dir: str = None) -> (int, int, List[str], List[str]):
        """Executes commands from cmd_list changing CWD to working_dir.

        :param cmd_list: list with command i.e. ['g4', '-option', ...]
        :param working_dir: if not None working directory is set to it for cmd exec

        :returns returns tuple. RC of executed command, elapsed execution time in secs, stdout lines, stderr lines
        """
        from subprocess import Popen, PIPE

        if working_dir:
            old_cwd = os.getcwd()
            os.chdir(working_dir)

        Log.dd('Executing: {cmd}'.format(cmd=' '.join(cmd_list)))
        Log.level_push()

        start_time = time.time()

        p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(None)
        rc = p.returncode

        # run your code
        elapsed_time_seconds = int(timedelta(seconds=int(time.time() - start_time)).total_seconds())

        if rc != 0:
            Log.w([
                'Command',
                '=======',
                ' '.join(cmd_list),
            ])

            if stdout.splitlines():
                Log.w([
                    'Command output (stdout)',
                    '=======================',
                ])
                _ = [Log.w('%r' % line) for line in stdout.splitlines()]

            if stderr.splitlines():
                Log.w([
                    'Command output (stderr)',
                    '=======================',
                ])
                _ = [Log.w('%r' % line) for line in stderr.splitlines()]

        # if rc != 0:
        #     print('Command output (stderr)')
        #     [Log.i('%r' % line) for line in err.splitlines()]

        if working_dir:
            # noinspection PyUnboundLocalVariable
            os.chdir(old_cwd)

        Log.dd('RC: {}'.format(rc))
        Log.level_pop()

        return rc, elapsed_time_seconds, stdout.splitlines(), stderr.splitlines()

    @staticmethod
    def remove_microseconds(delta: timedelta) -> timedelta:
        from datetime import timedelta
        return delta - timedelta(microseconds=delta.microseconds)

    @staticmethod
    def size_to_str(size_in_bytes: int, suffix: str = 'B') -> str:
        """Formats length in bytes into human readable string.
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(size_in_bytes) < 1024.0:
                if unit == '':
                    return '%d %s%s' % (size_in_bytes, unit, suffix)
                else:
                    return '%.1f %s%s' % (size_in_bytes, unit, suffix)
            size_in_bytes /= 1024.0
        return '%.1f %s%s' % (size_in_bytes, 'Yi', suffix)

    @staticmethod
    def size_to_int(val: str) -> int:
        """Parses size string trying to get size as int from it.

        Supported formats:
            "123" => 123
            "12k" => 12 * 1024
            "12M" => 12 * 1024 * 1024

        :param val: string representing sine
        :return: filesize

        :raise Raises InvalidArgument if cannot parse string
        """
        import re

        val = val.strip().replace(' ', '').lower()

        match = re.match(r'^([0-9]+)([bkmgt]?)$', val)
        if match is None:
            raise ValueError('Unable to parse provided size string %r' % val)

        unit = match.group(2) if match.group(2) != '' else 'b'
        return int(match.group(1)) * pow(1024, 'bkmgt'.find(unit))

    @staticmethod
    def md5(msg: str) -> str:
        """Calculates MD5 hashs for string argument.
        """
        import hashlib

        if str is None:
            raise ValueError('Data do hash cannot be None')

        name_hash = hashlib.md5()
        name_hash.update(msg.encode('UTF-8'))
        # return name_hash.digest()
        return name_hash.hexdigest()

    @staticmethod
    def get_class_data_type_key(class_name: str) -> str:
        """Builds class key string based on capital letters of class name i.e. for 'FooBarClass' would return 'fbc'.
        """
        data_type_key = ''
        for letter in class_name:
            if 'A' <= letter <= 'Z':
                data_type_key += letter

        return data_type_key.lower()

    @staticmethod
    def json_data_valid(json_dict: dict, required_type: str, required_min_version: int) -> bool:
        """Checks if given dict structure based on loaded JSON data matches requirements and is dump of our class
        """
        result = False
        if Const.FIELD_TYPE in json_dict:
            if json_dict[Const.FIELD_TYPE] == required_type:
                if Const.FIELD_VERSION in json_dict:
                    if json_dict[Const.FIELD_VERSION] >= required_min_version:
                        result = True

        return result

    @staticmethod
    def validate_env():
        import sys

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
