"""
ipvanish_bundle/core/exceptions.py
"""


class IPVanishBundleException(Exception):
    pass


class CountryNotFoundError(IPVanishBundleException):
    pass


class ConfigurationNotFound(IPVanishBundleException):
    pass
