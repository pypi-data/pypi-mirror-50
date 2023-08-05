"""PytSite Localization API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import yaml
import re
from typing import List, Callable, Dict
from importlib.util import find_spec
from copy import copy
from datetime import datetime
from os import path
from pytsite import threading, events
from . import _error

_languages = []
_current = {}  # Thread safe current language
_default = None  # type: str
_packages = {}
_globals = {}
_translated_strings_cache = {}

_ENG_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'

_ENG_IRREGULAR_PLURAL = {
    'child': 'children',
    'goose': 'geese',
    'man': 'men',
    'woman': 'women',
    'tooth': 'teeth',
    'foot': 'feet',
    'mouse': 'mice',
    'person': 'people',
}

_TL_CYRILLIC = [
    "Щ", "щ", 'Ё', 'Ж', 'Х', 'Ц', 'Ч', 'Ш', 'Ю', 'Я',
    'ё', 'ж', 'х', 'ц', 'ч', 'ш', 'ю', 'я', 'А', 'Б',
    'В', 'Г', 'Д', 'Е', 'З', 'И', 'Й', 'К', 'Л', 'М',
    'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Ь', 'Ы',
    'Ъ', 'Э', 'а', 'б', 'в', 'г', 'д', 'е', 'з', 'и',
    'і', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
    'т', 'у', 'ф', 'ь', 'ы', 'ъ', 'э', 'Ї', 'ї', 'Є',
    'є', 'Ґ', 'ґ']

_TL_ROMAN = [
    "Sch", "sch", 'Yo', 'Zh', 'Kh', 'Ts', 'Ch', 'Sh', 'Yu', 'Ya',
    'yo', 'zh', 'kh', 'ts', 'ch', 'sh', 'yu', 'ya', 'A', 'B',
    'V', 'G', 'D', 'E', 'Z', 'I', 'Y', 'K', 'L', 'M',
    'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', '', 'Y',
    '', 'E', 'a', 'b', 'v', 'g', 'd', 'e', 'z', 'i',
    'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
    't', 'u', 'f', '', 'y', '', 'e', 'i', 'i', 'Ye',
    'ye', 'G', 'g'
]

_SUB_TRANS_TOKEN_RE = re.compile('{:([_a-z0-9@]+)}')

_DEFAULT_REGIONS = {
    'en': 'US',
    'ru': 'RU',
    'uk': 'UA',
}


def _global_re_handler(match: re) -> str:
    f_name = match.group(1)
    if f_name not in _globals:
        return match.group(0)

    try:
        return _globals[f_name]()
    except Exception as e:
        raise RuntimeError('Error while calling lang function {}(): {}'.format(f_name, e))


def define(languages: list):
    """Define available languages
    """
    global _languages
    _languages = languages

    set_current(_languages[0])
    set_fallback(_languages[0])


def is_defined(language: str):
    """Check whether a language is defined.
    """
    return language in _languages


def langs(include_current: bool = True) -> List[str]:
    """Get all defined languages
    """
    r = _languages.copy()

    if not include_current:
        r.remove(_current[threading.get_id()])

    return r


def set_current(language: str):
    """Set current language
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    _current[threading.get_id()] = language


def set_fallback(language: str):
    """Set fallback language
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    global _default
    _fallback = language


def get_current() -> str:
    """Get current language
    """
    if not _languages:
        raise RuntimeError('No languages are defined')

    tid = threading.get_id()
    if tid not in _current:
        _current[threading.get_id()] = _languages[0]

    return _current[threading.get_id()]


def get_primary() -> str:
    """Get primary language
    """
    if not _languages:
        raise RuntimeError('There are no languages defined')

    return _languages[0]


def get_fallback() -> str:
    """Get fallback language
    """
    if not _languages:
        raise RuntimeError('No languages are defined')

    return _default


def is_package_registered(pkg_name):
    """Check if the package already registered
    """
    return pkg_name in _packages


def register_package(pkg_name: str, languages_dir: str = 'res/lang'):
    """Register language container
    """
    spec = find_spec(pkg_name)
    if not spec or not spec.loader:
        raise RuntimeError("Package '{}' is not found".format(pkg_name))

    lng_dir = path.join(path.dirname(spec.origin), languages_dir)
    if not path.isdir(lng_dir):
        raise RuntimeError("Language directory '{}' is not found".format(lng_dir))

    if pkg_name in _packages:
        raise _error.PackageAlreadyRegistered("Language package '{}' already registered".format(pkg_name))
    _packages[pkg_name] = {'__path': lng_dir}


def register_global(name: str, handler: Callable):
    """Register a global
    """
    if name in _globals:
        raise RuntimeError("Language global '{}' is already registered".format(name))

    if not callable(handler):
        raise TypeError("{} is not callable".format(type(handler)))

    _globals[name] = handler


def get_packages() -> dict:
    """Get info about registered packages
    """
    return _packages


def is_translation_defined(msg_id: str, language: str = None, use_fallback=True) -> bool:
    """Check if the translation is defined for message ID.
    """
    try:
        t(msg_id, None, language, True, use_fallback)
        return True
    except (_error.TranslationError, _error.PackageNotRegistered):
        return False


def english_plural(singular: str):
    if len(singular) < 2:
        return singular

    if singular in _ENG_IRREGULAR_PLURAL:
        return _ENG_IRREGULAR_PLURAL[singular]
    elif singular[-2:0] == 'on':
        return singular[:-2] + 'a'
    elif singular[-2:0] == 'is':
        return singular[:-2] + 'es'
    elif singular[-1] in ('s', 'x', 'z') or singular[-2:0] in ('sh', 'ch'):
        return singular + 'es'
    elif singular[-1] == 'f' or singular[-2:0] == 'fe':
        return singular[:-1] + 'ves'
    elif singular[-1] == 'y' and singular[-2] in _ENG_CONSONANTS:
        return singular[:-1] + 'ies'
    else:
        return singular + 's'


def transliterate(text: str, language: str = None) -> str:
    """Transliterate a string.
    """
    TL_ROMAN = _TL_ROMAN

    if language == 'uk':
        TL_ROMAN = copy(_TL_ROMAN)
        TL_ROMAN[_TL_CYRILLIC.index('Г')] = 'H'
        TL_ROMAN[_TL_CYRILLIC.index('И')] = 'Y'
        TL_ROMAN[_TL_CYRILLIC.index('Й')] = 'I'
        TL_ROMAN[_TL_CYRILLIC.index('г')] = 'h'
        TL_ROMAN[_TL_CYRILLIC.index('и')] = 'y'
        TL_ROMAN[_TL_CYRILLIC.index('й')] = 'i'

    r = ''
    for ch in text:
        try:
            i = _TL_CYRILLIC.index(ch)
            r += TL_ROMAN[i]
        except ValueError:
            r += ch

    return r


def t(msg_id: str, args: dict = None, language: str = None, exceptions: bool = False, use_fallback: bool = True) -> str:
    """Translate a message
    """
    global _globals

    if not language:
        language = get_current()

    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    if msg_id in _globals:
        return _globals[msg_id](language, args)

    # Determining package name and message ID
    package_name, msg_id = _split_msg_id(msg_id)

    # Try to get message translation string from cache
    cache_key = '{}-{}@{}'.format(language, package_name, msg_id)
    msg = _translated_strings_cache.get(cache_key)

    # Message translation is not found in cache, try to fetch it
    if not msg:
        # Try to get translation via event
        for r in events.fire('pytsite.lang@translate', language=language, package_name=package_name, msg_id=msg_id):
            msg = r

        # Load translation from package's data
        if not msg:
            lang_file_content = get_package_translations(package_name, language)

            if msg_id not in lang_file_content:
                # Searching for fallback translation
                fallback = get_fallback()
                if use_fallback and fallback != language:
                    return t(package_name + '@' + msg_id, args, fallback, exceptions, False)
                else:
                    if exceptions:
                        raise _error.TranslationError(
                            "Translation is not found for '{}@{}'".format(package_name, msg_id))
                    else:
                        return package_name + '@' + msg_id

            msg = lang_file_content[msg_id]

        # Cache translation string
        _translated_strings_cache[cache_key] = msg

    # Replace placeholders
    if args:
        for k, v in args.items():
            msg = msg.replace(':' + str(k), str(v))

    # Replace sub-translations
    msg = _SUB_TRANS_TOKEN_RE.sub(lambda match: t(match.group(1)), msg)

    return msg


def t_plural(msg_id: str, num: int = 2, language: str = None) -> str:
    """Translate a string in plural form.
    """
    if not language:
        language = get_current()

    # Language is English
    if language == 'en':
        return t(msg_id + '_plural_{}'.format('one' if num == 1 else 'two'))

    suffix = 'zero'
    num = num if num < 100 else int(str(num)[-2:])  # Get only last two digits
    if not 5 <= num <= 20:
        last_digit = int(str(num)[-1])
        if last_digit == 1:
            suffix = 'one'
        elif 1 < last_digit < 5:
            suffix = 'two'

    return t(msg_id + '_plural_' + suffix)


def lang_title(language: str = None) -> str:
    """Get human readable language name
    """
    if not language:
        language = get_current()

    try:
        return t('pytsite.lang@lang_title_' + language, exceptions=True)
    except _error.TranslationError:
        try:
            return t('app@lang_title_' + language, exceptions=True)
        except _error.TranslationError:
            return language


def get_package_translations(pkg_name: str, language: str = None) -> Dict[str, str]:
    """Load package's language file
    """
    # Is the package registered?
    if not is_package_registered(pkg_name):
        plugins_pkg_name = 'plugins.' + pkg_name
        if is_package_registered(plugins_pkg_name):
            pkg_name = plugins_pkg_name
        else:
            raise _error.PackageNotRegistered("Language package '{}' is not registered".format(pkg_name))

    if not language:
        language = get_current()

    # Getting from cache
    if language in _packages[pkg_name]:
        return _packages[pkg_name][language]

    content = {}

    # Actual data loading
    file_path = path.join(_packages[pkg_name]['__path'], language + '.yml')
    if not path.exists(file_path):
        return content

    with open(file_path, encoding='utf-8') as f:
        content = yaml.load(f, yaml.FullLoader)

    if content is None:
        content = {}

    # Caching
    _packages[pkg_name][language] = content

    return content


def time_ago(time: datetime) -> str:
    """Format date/time as 'time ago' phrase.
    """
    diff = datetime.now() - time
    """:type: datetime.timedelta"""

    if diff.days:
        if diff.days > 365:
            years = diff.days // 365
            return '{} {}'.format(years, t_plural('pytsite.lang@year', years))
        elif diff.days > 31:
            months = diff.days // 12
            return '{} {}'.format(months, t_plural('pytsite.lang@month', months))
        elif diff.days > 7:
            weeks = diff.days // 7
            return '{} {}'.format(weeks, t_plural('pytsite.lang@week', weeks))
        else:
            return '{} {}'.format(diff.days, t_plural('pytsite.lang@day', diff.days))
    else:
        if diff.seconds > 3600:
            hours = diff.seconds // 3600
            return '{} {}'.format(hours, t_plural('pytsite.lang@hour', hours))
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return '{} {}'.format(minutes, t_plural('pytsite.lang@minute', minutes))
        else:
            if diff.seconds:
                return '{} {}'.format(diff.seconds, t_plural('pytsite.lang@second', diff.seconds))
            else:
                return t('pytsite.lang@just_now')


def pretty_date(date_time: datetime) -> str:
    """Format date as pretty string.
    """
    r = '{} {}'.format(date_time.day, t_plural('pytsite.lang@month_' + str(date_time.month)))

    if date_time.now().year != date_time.year:
        r += ' ' + str(date_time.year)

    return r


def pretty_date_time(time: datetime) -> str:
    """Format date/time as pretty string.
    """
    return '{}, {}'.format(pretty_date(time), time.strftime('%H:%M'))


def ietf_tag(language: str = None, region: str = None, sep: str = '-') -> str:
    global _DEFAULT_REGIONS

    if not language:
        language = get_current()

    if not region:
        region = _DEFAULT_REGIONS[language] if language in _DEFAULT_REGIONS else language

    return language.lower() + sep + region.upper()


def on_translate(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.lang@translate', handler, priority)


def on_split_msg_id(handler, priority: int = 0):
    """Shortcut
    """
    events.listen('pytsite.lang@split_msg_id', handler, priority)


def clear_cache():
    """Clear translations cache
    """
    global _translated_strings_cache

    _translated_strings_cache = {}


def _split_msg_id(msg_id: str) -> list:
    """Split message ID into message ID and package name.
    """
    for r in events.fire('pytsite.lang@split_msg_id', msg_id=msg_id):
        msg_id = r

    return msg_id.split('@')[:2] if '@' in msg_id else ['app', msg_id]
