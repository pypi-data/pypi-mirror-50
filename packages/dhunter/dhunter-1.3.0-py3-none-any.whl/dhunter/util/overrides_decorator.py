# coding=utf8

"""

 dhunter

 Fast, content based duplicate file detector with cache and more!
 Copyright ©2018-2019 Marcin Orlowski <mail [@] MarcinOrlowski.com>

 https://github.com/MarcinOrlowski/dhunter

"""


def overrides(interface_class) -> callable:
    def overrider(method):
        """Introduces @overrides decorator.
        Source: https://stackoverflow.com/a/8313042
        """
        assert method.__name__ in dir(interface_class), \
            "No '{name}()' to override in '{cls}' class".format(name=method.__name__, cls=interface_class.__name__)
        return method

    return overrider
