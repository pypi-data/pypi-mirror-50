""" Python wrapper for Buyproxies.org API """

__author__ = "Maciej Janowski"

import requests


class BuyProxiesAPI:
    """
    Retrieve proxies
    """
    URL = 'http://api.buyproxies.org/'

    def __init__(self, api_key):
        """ Initialize with API Key """
        self.API_KEY = api_key

    def get_proxies(self, service_id: int, return_as='list', proxy_format=1):
        """
        Retrieves a list of proxies for selected service in one of 4 formats
        :param service_id: ID of Proxy service on
        :param return_as: Specifies format of returned proxies | json - json object | list - python list | str - String
        :param proxy_format: 1 - user:pass:ip:port | 2 - user:pass@ip:port | 3 - ip:port
        :return: List of proxies
        """
        endpoint = f'?a=showProxies&pid={service_id}&key={self.API_KEY}&format={proxy_format}'
        response = self.__make_request(BuyProxiesAPI.URL + endpoint)
        if response:
            text = response.text
            return_dict = {
                'list': self.__to_list(text),
                'json': self.__to_json(self.__to_list(text)),
                'str': text
            }
            # TODO Raise error if return_as is not in return_dict
            return return_dict[return_as]

        return []

    @staticmethod
    def __to_list(text):
        """
        Convert string to list by spliting it on new line
        :param text: string with proxies each proxy on new line
        :return: list of strings
        """
        return text.split('\n')

    @staticmethod
    def __to_json(proxy_lst):
        """
        Turn list of strings to json format
        :param proxy_lst: list of proxies strings
        :return: json formatted list
        """
        return {
            "proxies": proxy_lst
        }

    @staticmethod
    def __make_request(url):
        """
        Make HTTP GET Request
        :param url: string with url
        :return: Response object or None if request fails
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response
        print(f"HTTP Request to URL: {url} failed with {response.status_code} status code")
        return None
