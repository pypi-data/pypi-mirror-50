"""
"""
import sys

from typing import List

from ipvanish_bundle.core import utils


def filter(country: str, exclude: List[str] = list) -> List[str]:
    """

    :param country: str -
    :param exclude: str -
    :return: List[str] -
    """
    country_dir = utils.get_country_dir(__file__, sys.platform)
    country_module = utils.get_country_module(country, country_dir)
    return utils.filter_country_module(country_module, exclude=exclude)


def get_by_country_name(country: str, name: str) -> List[str]:
    """

    :param country: str -
    :param name: str -
    :return: List[str] -
    """
    country_dir = utils.get_country_dir(__file__, sys.platform)
    country_module = utils.get_country_module(country, country_dir)
    return utils.get_by_country_name(country_module, name)
