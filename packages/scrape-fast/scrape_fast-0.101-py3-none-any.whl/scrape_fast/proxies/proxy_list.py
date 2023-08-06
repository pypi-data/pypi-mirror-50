""" Proxies operations """
from random import choice


class Proxy:
    """ Proxy model """

    def __init__(self, proxy):
        self.proxy = proxy

    def json(self):
        """ Returns json representation of the proxy"""
        return {
            'http': 'http://' + self.proxy,
            'https': 'http://' + self.proxy
        }


class ProxyList:
    """ Proxy handling class """

    def __init__(self, proxies=None):
        """
        :param proxies: List of additional proxies you want to initialize the list with
        """
        if proxies is None:
            proxies = list()
        self.proxies = proxies

    def read_from_file(self, filename):
        """
        Reads a text file with one proxy per line and adds proxies to the list
        :param filename:
        """
        with open(filename, 'r') as file:
            self.proxies += [x for x in file.read().splitlines() if x.strip()]

    def get_random_proxy(self):
        """ return a random proxy in a dictionary
        :return: Proxy dictionary
        """
        random_proxy = choice(self.proxies)
        return Proxy(random_proxy).json()
