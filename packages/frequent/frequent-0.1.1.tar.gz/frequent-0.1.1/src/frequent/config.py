# -*- coding: utf-8 -*-
#
#   This module is part of the Frequent project, Copyright (C) 2019,
#   Douglas Daly.  The Frequent package is free software, licensed under
#   the MIT License.
#
#   Source Code:
#       https://github.com/douglasdaly/frequent-py
#   Documentation:
#       https://frequent-py.readthedocs.io/en/latest
#   License:
#       https://frequent-py.readthedocs.io/en/latest/license.html
#
"""
Configuration module for global configuration settings.
"""
from collections.abc import MutableMapping
from contextlib import contextmanager
from copy import copy
from functools import wraps
import json
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterator as T_Iterator
from typing import Optional
from typing import Tuple
from typing import Type

__all__ = [
    'Configuration',
    'clear_config',
    'get_config',
    'load_config',
    'save_config',
    'set_config',
    'temp_config',
]


_GLOBAL_CONFIG: Optional['Configuration'] = None


def _make_sentinel(name: str = '_MISSING') -> 'Sentinel':
    """Creates a new sentinel object, code adapted from boltons:
        https://github.com/mahmoud/boltons/
    """
    class Sentinel(object):
        def __init__(self):
            self.name = name

        def __repr__(self):
            return '%s(%r)' % (self.__class__.__name__, self.name)

        def __nonzero__(self):
            return False

        __bool__ = __nonzero__

    return Sentinel()


_MISSING = _make_sentinel()


class Configuration(MutableMapping):
    """
    Configuration storage object.

    This object is basically a :obj:`dict` with some additional bells
    and whistles, including:

    - The ability to access/modify items like attributes.
    - Serialize to/from strings via `dumps` and `loads`.
    - `save` and `load` to/from files.
    - Easily convert standard :obj:`dict` objects with `to_dict` and
      `from_dict`.

    Examples
    --------
    This object works like a :obj:`dict`, where settings can be
    retrieved and set using:

    >>> config = Configuration()
    >>> config['answer'] = 42
    >>> config['answer']
    42

    Additionally, you can nest settings using the `.` as a seperator,
    for instance:

    >>> config['nested.setting'] = 'value'
    >>> config['nested']
    {'setting': 'value'}
    >>> config['nested.setting']
    'value'
    >>> config['nested']['setting']
    'value'

    Furthermore, you can work with settings as if they were attributes:

    >>> config.nested.setting
    'value'
    >>> config.dirs.temp = '/home/doug/tmp'
    >>> config['dirs.temp']
    '/home/doug/tmp'

    """
    __key_seperator__ = '.'

    def __init__(self, *args, **kwargs) -> None:
        self._storage = dict()
        return super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} settings={repr(self._storage)}>"

    def __getitem__(self, key: str) -> Any:
        key, subkey = self._key_helper(key)
        rv = self._storage[key]
        if subkey:
            rv = rv[subkey]
        return rv

    def __setitem__(self, key: str, value: Any) -> None:
        key, subkey = self._key_helper(key)
        if isinstance(value, dict):
            value = self.__class__(value)
        if subkey:
            if key not in self._storage:
                self._storage[key] = self.__class__()
            self._storage[key][subkey] = value
        else:
            self._storage[key] = value
        return

    def __delitem__(self, key: str) -> None:
        key, subkey = self._key_helper(key)
        if subkey:
            del self._storage[key][subkey]
        else:
            del self._storage[key]
        return

    def __len__(self) -> int:
        return len(self._storage)

    def __iter__(self) -> T_Iterator:
        return iter(self._storage)

    def __getattr__(self, name: str) -> Any:
        try:
            rv = super().__getattribute__(name)
        except AttributeError as ex:
            try:
                rv = self[name]
            except KeyError:
                raise ex
        return rv

    def __setattr__(self, name: str, value: Any) -> None:
        if name != '_storage' and name not in self.__dict__:
            return self.__setitem__(name, value)
        return super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        if name == '_storage':
            raise Exception('Cannot delete _storage object')
        elif name not in self.__dict__:
            return self.__delitem__(name)
        return super().__delattr__(name)

    def clear(self) -> None:
        """Clears all the settings stored in this configuration."""
        return self._storage.clear()

    def copy(self) -> 'Configuration':
        """Creates a copy of this configuration object.

        Returns
        -------
        Configuration
            A copy of this configuration object.

        """
        rv = self.__class__()
        rv.update(copy(self._storage))
        return rv

    def dumps(self, compact: bool = True, **kwargs) -> str:
        """Serializes this configuration object to a string.

        The default method uses the built-in python json library to
        convert this configuration to a JSON string.  To use another
        method or format override this method.

        Parameters
        ----------
        compact : bool, optional
            Make the returned representation as compact as possible
            (default is :obj:`True`).

        Returns
        -------
        str
            String-serialized representation of this configuration.

        """
        json_kws = {}
        json_kws['sort_keys'] = True
        if not compact:
            json_kws['indent'] = 2
        json_kws.update(kwargs)
        return json.dumps(self.to_dict(), **json_kws)

    @classmethod
    def loads(cls, text: str, **kwargs) -> 'Configuration':
        """Creates a new configuration from the given string data.

        Parameters
        ----------
        text : str
            String-serialized representation to create the new object
            from.

        Returns
        -------
        Configuration
            The newly created configuration from the given string data.

        """
        data = json.loads(text, **kwargs)
        return cls.from_dict(data)

    def save(self, path: str, **kwargs) -> None:
        """Saves this configuration object to the file path specified.

        Parameters
        ----------
        path : str
            File path to save the configuration object to.
        kwargs : optional
            Additional parameters to pass through to the `dumps` call.

        See Also
        --------
        dumps

        """
        with open(path, 'w') as fout:
            fout.write(self.dumps(compact=False, **kwargs))
        return

    @classmethod
    def load(cls, path: str, **kwargs) -> 'Configuration':
        """Loads a configuration object from the file path specified.

        Parameters
        ----------
        path : str
            File path to load the configuration object from.
        kwargs : optional
            Additional parameters to pass through to the `loads` call.

        Returns
        -------
        Configuration
            The :obj:`Configuration` object loaded from the `path`
            given.

        See Also
        --------
        loads

        """
        with open(path, 'r') as fin:
            text = fin.readlines()
        return cls.loads(''.join(text), **kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Configuration':
        """Creates a configuration object from the given :obj:`dict`.

        Parameters
        ----------
        data : dict
            Dictionary to generate the new configuration object with.

        Returns
        -------
        Configuration
            The new configuration from the given dictionary data.

        """
        rv = cls()
        for k, v in data.items():
            if isinstance(v, dict):
                v = cls.from_dict(v)
            rv[k] = v
        return rv

    def to_dict(self) -> Dict[str, Any]:
        """Converts this configuration object to a standard :obj:`dict`.

        Returns
        -------
        dict
            Standard :obj:`dict` version of this configuration object.

        """
        rv = {}
        for k, v in self.items():
            if isinstance(v, Configuration):
                v = v.to_dict()
            rv[k] = v
        return rv

    @classmethod
    def _key_helper(cls, key: str) -> Tuple[str, str]:
        """Splits the given key into a key & subkey"""
        if cls.__key_seperator__ in key:
            r_key, r_subkey = key.split(cls.__key_seperator__, 1)
        else:
            r_key = key
            r_subkey = None
        return r_key, r_subkey


def load_config(
    path: str = None, config_cls: Type[Configuration] = Configuration
) -> None:
    """Loads the global configuration from the given file path.

    Parameters
    ----------
    path : str, optional
        The file path to load the configuration file from.  If this is
        not provided a new, empty :obj:`Configuration` is loaded.
    config_cls : type, optional
        The type of :obj:`Configuration` to load (the default is the
        standard :obj:`Configuration` class).

    """
    global _GLOBAL_CONFIG
    if path:
        _GLOBAL_CONFIG = config_cls.load(path)
    else:
        _GLOBAL_CONFIG = config_cls()
    return


def _ensure_config(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _GLOBAL_CONFIG
        if _GLOBAL_CONFIG is None:
            load_config()
        return f(*args, **kwargs)
    return wrapper


@_ensure_config
def save_config(path: str) -> None:
    """Saves the current global configuration to the given file path.

    Parameters
    ----------
    path : str
        The file path to save the configuration to.

    """
    global _GLOBAL_CONFIG
    return _GLOBAL_CONFIG.save(path)


@_ensure_config
def get_config(name: str = None, default: Any = _MISSING) -> Any:
    """Gets the global configuration.

    Parameters
    ----------
    name : str, optional
        The name of the setting to get the value for.  If no name is
        given then the whole :obj:`Configuration` object is returned.
    default : optional
        The default value to return if `name` is provided but the
        setting doesn't exist in the global configuration.

    Returns
    -------
    :obj:`Configuration` or :obj:`object`
        The global configuration object or the configuration setting
        requested.

    """
    global _GLOBAL_CONFIG
    if not name:
        return _GLOBAL_CONFIG.copy()
    if default == _MISSING:
        return _GLOBAL_CONFIG[name]
    return _GLOBAL_CONFIG.get(name, default)


@_ensure_config
def set_config(name: str, value: Any) -> None:
    """Sets a configuration setting.

    Parameters
    ----------
    name : str
        The setting to set the `value` for.
    value : object
        The value to set for the given `name`.

    """
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG[name] = value
    return


def clear_config() -> None:
    """Clears the currently-set global configuration."""
    global _GLOBAL_CONFIG
    if _GLOBAL_CONFIG is not None:
        _GLOBAL_CONFIG.clear()
        _GLOBAL_CONFIG = None
    return


@contextmanager
@_ensure_config
def temp_config(**settings) -> Configuration:
    """Gets a context with a temporary configuration.

    Any changes made to the configuration via calls to :obj:`set_config`
    (or otherwise) will be made and persisted only within the context.
    The original configuration will be restored upon leaving the
    context.

    Parameters
    ----------
    settings : optional
        Any temporary settings to set in the temporary configuration
        context.

    Yields
    ------
    Configuration
        The temporary configuration object.

    """
    global _GLOBAL_CONFIG
    curr_config = _GLOBAL_CONFIG.copy()
    try:
        for k, v in settings.items():
            set_config(k, v)
        yield _GLOBAL_CONFIG.copy()
    finally:
        _GLOBAL_CONFIG = curr_config
    return
