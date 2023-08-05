# coding=utf8

"""

 File Deduper

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/file-deduper

"""
import sys

if __name__ == '__main__':
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
    app.main()
