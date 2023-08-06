"""
ipvanish_bundle/core/utils.py
"""

import os
import importlib.util

from typing import List

from ipvanish_bundle.core.exceptions import CountryNotFoundError, ConfigurationNotFound


def get_country_dir(file_path: str, platform: str) -> str:
    """

    :param file_path: str -
    :param platform: str -
    :return: str -
    """
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(file_path))),
                        'bundle',
                        platform)


def get_country_module(country: str, country_dir: str) -> object:
    """

    :param country: str -
    :param country_dir: str -
    :return: object -
    :raises: CountryNotFoundError -
    """
    mod = None
    country_lowercase = country.lower()

    # Get all modules in current dir
    for f in os.listdir(country_dir):
        # Skip some files by default
        if f.startswith('.') or f.startswith('__') or not f.endswith('.py'):
            continue

        # Check the country code
        if country_lowercase == f.replace('.py', '').lower():
            spec = importlib.util.spec_from_file_location(country_lowercase,
                                                          os.path.join(country_dir, f))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            break

    if mod is None:
        raise CountryNotFoundError(f'Country module Not Found: {country}')

    return mod


def filter_country_module(country_module: object, exclude: List[str] = list) -> List[str]:
    """

    :param country_module: object -
    :param exclude: List[str] -
    :return: List[str] -
    """
    ret = []
    for attr in dir(country_module):
        if attr.startswith('__'):
            continue
        if attr not in exclude:
            ret.append(attr)

    return ret


def get_by_country_name(country_module: object, config_name: str) -> List[str]:
    """

    :param country_module: object -
    :param config_name: str -
    :return: List[str] -
    :raises: ConfigurationNotFound -
    """
    ret = None
    for att in dir(country_module):
        if att == config_name:
            ret = getattr(country_module, att)

    if not ret:
        raise ConfigurationNotFound(f'Not Found: {config_name}')
    return ret
