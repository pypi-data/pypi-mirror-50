""" Python wrapper for Buyproxies.org API """

import requests

from buyproxies_api.errors import EmptyResponseError


class BuyProxiesAPI:
    """
    Retrieve proxies
    """
    URL = 'http://api.buyproxies.org/'

    def __init__(self, api_key):
        """ Initialize with API Key """
        self.API_KEY = api_key

    def get_proxies(self, service_id: int, return_as: str = 'list', proxy_format: int = 1):
        """
        Retrieves a list of proxies for selected service in one of 4 formats
        :param service_id: ID of Proxy service on
        :param return_as: Specifies format of returned proxies | json - json object | list - python list | str - String
        :param proxy_format: 1 - user:pass:ip:port | 2 - user:pass@ip:port | 3 - ip:port
        :return: List of proxies
        """
        if type(service_id) is not int:
            raise TypeError("`service_id` has to be an int.")
        if type(return_as) is not str:
            raise TypeError("`return_as` has to be a string.")
        if return_as not in ['list', 'json', 'str']:
            raise TypeError('{} is not a valid value for `return_as` parameter. Valid values: "json", "list", "str".'
                            .format(return_as))
        if type(proxy_format) is not int:
            raise TypeError("`proxy_format' has to be an int.")
        if proxy_format not in range(1,4):
            raise ValueError("`proxy_format` value can only be 1, 2 or 3.")

        endpoint = f'?a=showProxies&pid={service_id}&key={self.API_KEY}&format={proxy_format}'
        response = self.__make_request(BuyProxiesAPI.URL + endpoint)

        text = response.text.strip()
        if text is None:
            error_str = "Request returned empty response check if your api key or service id is correct or if your service is active."
            raise EmptyResponseError(error_str)
        return_dict = {
            'list': self.__to_list(text),
            'json': self.__to_json(self.__to_list(text)),
            'str': text
        }

        return return_dict[return_as]

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
        try:
            response = requests.get(url)
        except Exception as e:
            raise ConnectionError("Request to Buyproxies.org failed, with: {}".format(e))
        if response.status_code == 200:
            return response
        raise ConnectionError(f"HTTP Request to URL: {url} failed with {response.status_code} status code")
