from typing import Dict, List, Union

import requests
from requests import Response


class Client:

    def __init__(self, headers: Dict['str', 'str']):
        self.headers: Dict['str', 'str'] = headers

    def get(self, url: str, params: Dict = None) -> Union[Dict, List]:
        response: Response = requests.get(url=url, params=params, headers=self.headers)
        body = self.__handle_response(response)
        return body

    def post(self, url: str, data: Dict) -> Union[Dict, List]:
        response: Response = requests.post(url=url, data=data, headers=self.headers)
        body = self.__handle_response(response)
        return body

    def put(self, url: str, data: Dict) -> Union[Dict, List]:
        response: Response = requests.put(url=url, data=data, headers=self.headers)
        body = self.__handle_response(response)
        return body

    def delete(self, url: str):
        response: Response = requests.delete(url=url)
        self.__validate_response(response)

    def __handle_response(self, response) -> Union[Dict, List]:
        self.__validate_response(response)
        body = response.json()
        return body

    @staticmethod
    def __validate_response(response: Response):
        if response.status_code > 400:
            raise Exception(f'an error occurred on {response.url}')
