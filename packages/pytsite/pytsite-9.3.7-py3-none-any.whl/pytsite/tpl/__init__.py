"""PytSite Templates Support
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
import jinja2
import json
from typing import Mapping
from datetime import datetime
from importlib.util import find_spec as find_module_spec
from os import path
from urllib.parse import urlparse
from pytsite import reg as reg, lang, util, events, package_info
from . import _error as error

_packages = {}


def _resolve_location(location: str) -> list:
    for r in events.fire('pytsite.tpl@resolve_location', location=location):
        location = r

    if '@' in location:
        return location.split('@')[:2]
    else:
        return ['app', location]


def _resolve_name(tpl_name: str) -> str:
    for r in events.fire('pytsite.tpl@resolve_name', tpl_name=tpl_name):
        tpl_name = r or tpl_name

    return tpl_name


def _get_path(location: str) -> str:
    if not location:
        raise ValueError('Template name is not specified')

    pkg_name, tpl_name = _resolve_location(location)

    if pkg_name not in _packages:
        plugin_pkg_name = 'plugins.' + pkg_name
        if plugin_pkg_name in _packages:
            pkg_name = plugin_pkg_name
        else:
            raise error.TemplateNotFound("Templates package '{}' is not registered".format(pkg_name))

    if not tpl_name.endswith('.jinja2'):
        tpl_name += '.jinja2'

    return path.join(_packages[pkg_name]['templates_dir'], tpl_name)


def tpl_exists(tpl: str) -> bool:
    return path.exists(_get_path(tpl))


class _TemplateLoader(jinja2.BaseLoader):
    """Template Loader
    """

    def get_source(self, environment, tpl: str) -> tuple:
        tpl_path = _get_path(tpl)

        if not tpl_exists(tpl):
            raise error.TemplateNotFound("Template is not found at '{}'".format(tpl_path))

        with open(tpl_path, encoding='utf-8') as f:
            source = f.read()

        return source, tpl_path, lambda: False


_env = jinja2.Environment(loader=_TemplateLoader(), extensions=['jinja2.ext.do'])


def _date_filter(value: datetime, fmt: str = 'pretty_date') -> str:
    if not value:
        value = datetime.now()

    if fmt == 'pretty_date':
        return lang.pretty_date(value)
    elif fmt == 'pretty_date_time':
        return lang.pretty_date_time(value)
    else:
        return value.strftime(fmt)


def register_package(package_name: str, templates_dir: str = 'res/tpl', alias: str = None):
    """Register templates container.
    """
    if package_name in _packages:
        raise RuntimeError("Package '{}' already registered".format(package_name))

    pkg_spec = find_module_spec(package_name)
    if not pkg_spec:
        raise RuntimeError("Package '{}' is not found".format(package_name))

    templates_dir = path.join(path.dirname(pkg_spec.origin), templates_dir)
    if not path.isdir(templates_dir):
        raise NotADirectoryError("Directory '{}' is not found".format(templates_dir))

    config = {'templates_dir': templates_dir}
    _packages[package_name] = config

    if alias:
        _packages[alias] = config


def render(template: str, args: Mapping = None, emit_event: bool = True) -> str:
    """Render a template
    """
    if not args:
        args = {}

    if emit_event:
        events.fire('pytsite.tpl@render', tpl_name=template, args=args)

    return _env.get_template(template).render(args)


def on_render(handler, priority: int = 0):
    """Shortcut function to register event handler
    """
    events.listen('pytsite.tpl@render', handler, priority)


def is_global_registered(name: str) -> bool:
    """Check if the global registered.
    """
    return name in _env.globals


def register_global(name: str, obj):
    """Register global.
    """
    _env.globals[name] = obj


def on_resolve_location(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.tpl@resolve_location', handler, priority)


def on_resolve_name(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.tpl@resolve_name', handler, priority)


# Additional functions and filters
_env.globals['tpl_exists'] = tpl_exists
_env.globals['t'] = lang.t
_env.globals['t_plural'] = lang.t_plural
_env.globals['langs'] = lang.langs
_env.globals['current_lang'] = lang.get_current
_env.globals['reg_get'] = reg.get
_env.globals['nav_link'] = util.nav_link
_env.globals['url_parse'] = urlparse
_env.globals['app_name'] = lambda: reg.get('app.app_name_' + lang.get_current(), 'PytSite')
_env.globals['app_version'] = package_info.version('app')
_env.filters['date'] = _date_filter
_env.filters['nl2br'] = lambda value: value.replace('\n', jinja2.Markup('<br>'))
_env.filters['tojson'] = lambda obj: json.dumps(obj)
