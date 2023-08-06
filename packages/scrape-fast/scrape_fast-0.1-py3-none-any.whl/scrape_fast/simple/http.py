""" Simple HTTP GET request"""
import json
from time import sleep
from random import uniform

import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 " \
             "(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT
}


def make_request(url, output='r', headers=None, proxies=None, random_delay=(0, 0), retry_count=0, max_retries=3):
    """
    Makes HTTP GET request
    :param url: string with url address,
    :param headers: default None else headers dictionary
    :param proxies: proxies dictionary
    :param output: string defining returned format, r - Response, j - json, b - BeautifulSoup
    :param random_delay: tuple representing range of seconds to wait randomly after request
    :return: if successful Response object or one of its methods else None
    :param retry_count: Used to keep of track of recursive retries
    :param max_retries: Used to set maximum amount of recursive retries
    """
    response = requests.get(url=url,
                            headers=headers if headers else DEFAULT_HEADERS,
                            proxies=proxies)
    sleep(uniform(*random_delay))
    # Check if request was successful
    if response.status_code == 200:
        return define_output(response, output)
    elif response.status_code in [522, 403]:  # TODO Add more status codes
        print("RETRYING REQUEST ({})".format(response.status_code), url)
        return make_request(url, output, headers,
                            random_delay, retry_count, max_retries)

    print("FAILED REQUEST ({})".format(response.status_code), url)
    return None


def define_output(response, output):
    """ Defines make_request output
    :param response: Response object
    :param output: String defining returned format
    :return: Response object, one of its methods or None
    """
    options = {
        'r': response,
        'j': response_to_json(response),
        'b': BeautifulSoup(response.content, 'html.parser')
    }
    return options[output]


def response_to_json(response):
    """
    Tries to get json from Response
    :param response: Response object
    :return: json data or None
    """
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        return None
