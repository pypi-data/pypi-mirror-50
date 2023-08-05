"""PytSite pip Support API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import subprocess
import json
from semaver import VersionRange
from pytsite import reg
from . import _error

_DEBUG = reg.get('debug')
_installed_packages = {}


def ls(outdated: bool = False) -> dict:
    """Get list of installed packages
    """
    cmd = ['pip', 'list', '--format=json']

    if outdated:
        cmd.append('--outdated')

    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return json.loads(r.stdout)


def show(pkg_name: str) -> dict:
    """Get installed package's info
    """
    cmd = ['pip', 'show', pkg_name]

    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if r.returncode != 0:
        raise _error.PackageNotInstalled(pkg_name)

    data = {}
    for r_str in r.stdout.decode('utf-8').split('\n'):
        r_str_split = r_str.split(':')
        k = r_str_split[0].strip().lower()
        if k:
            data[k] = ':'.join(r_str_split[1:]).strip()

    return data


def is_installed(pkg_name: str, pkg_version: VersionRange) -> bool:
    """Check if the package is installed
    """
    if (pkg_name, str(pkg_version)) not in _installed_packages:
        try:
            _installed_packages[(pkg_name, str(pkg_version))] = show(pkg_name)['version'] in pkg_version
        except _error.PackageNotInstalled:
            _installed_packages[(pkg_name, str(pkg_version))] = False
            return False

    return _installed_packages[(pkg_name, str(pkg_version))]


def install(pkg_name: str, v_range: VersionRange = None, upgrade: bool = False, passthrough: bool = _DEBUG) -> int:
    """Install a package
    """
    cmd = ['pip', 'install']

    if v_range:
        pkg_name += str(v_range)

    if upgrade:
        cmd.append('-U')

    cmd.append(pkg_name)

    stdout = stderr = None if passthrough else subprocess.PIPE

    r = subprocess.run(cmd, stdout=stdout, stderr=stderr)
    if r.returncode != 0:
        raise _error.PackageInstallError('{} {}'.format(pkg_name, v_range),
                                         r.stderr.decode('utf-8') if r.stderr else None)

    return r.returncode


def uninstall(pkg_name: str) -> str:
    """Uninstall a package
    """
    r = subprocess.run(['pip', 'uninstall', '-y', pkg_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if r.returncode != 0:
        raise _error.PackageUninstallError(pkg_name, r.stderr.decode('utf-8'))

    return r.stdout.decode('utf-8')
