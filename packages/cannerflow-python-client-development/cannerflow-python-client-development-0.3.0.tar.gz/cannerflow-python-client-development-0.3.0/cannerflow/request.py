import requests
__all__ = ["Request"]

class Request():
    def __init__(
        self,
        endpoint,
        headers
    ):
        self._endpoint = endpoint
        self._headers = headers
    def getUrl(self):
        return "{endpoint}/{path}".format(
            endpoint=self._endpoint,
            path='graphql'
        )
    def post(self, payload):
        http_response = {}
        try:
            http_response = requests.post(
                self.getUrl(),
                json=payload,
                headers=self._headers
            )
            http_response.raise_for_status()
        except Exception as err:
            print(f'Error occured: {err}, {http_response.content}')
        else:
            data = http_response.json()
            if "error" in data:
                print(f'Error occured: {data.error}')
            return data.get('data')
