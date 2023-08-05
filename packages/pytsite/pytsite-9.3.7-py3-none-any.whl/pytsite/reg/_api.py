"""PytSite Registry API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .driver import Abstract as AbstractDriver

_current_driver = None  # type: _Driver


def set_driver(driver: AbstractDriver):
    """Switch registry driver
    """
    global _current_driver

    _current_driver = driver


def get_driver() -> AbstractDriver:
    if not _current_driver:
        raise RuntimeError('Registry driver is not set')

    return _current_driver


def put(key: str, value):
    """Set value
    """
    try:
        _current_driver.put(key, value)
    except AttributeError:
        raise RuntimeError('Registry driver is not set')


def get(key: str, default=None):
    """Get value
    """
    try:
        return _current_driver.get(key, default)
    except AttributeError:
        raise RuntimeError('Registry driver is not set')
