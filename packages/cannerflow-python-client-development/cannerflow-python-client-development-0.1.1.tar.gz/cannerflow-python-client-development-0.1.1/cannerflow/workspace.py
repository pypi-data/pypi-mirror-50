import requests


class Workspace(object):
    def __init__(
        self,
        endpoint,
        headers,
        workspaceId
    ):
        self.endpoint = endpoint
        self.headers = headers
        self.workspaceId = workspaceId
        request = ApplicationRequest(
            headers=headers,
            endpoint=endpoint
        )
        self.request=request
        self.savedQuery = SavedQuery(
            request=request,
            workspaceId=workspaceId
        )


class ApplicationRequest():
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

class SavedQuery(object):
    def __init__(
        self,
        workspaceId,
        request
    ):
        self.workspaceId = workspaceId
        self.request = request
    def getPayload(self):
        return {
            'operationName': 'sqls',
            'query': """
                query sqls($where: SqlWhereInput!) {
                    sqls(where: $where) {
                        id
                        sql
                        title
                        description
                        workspaceId
                    }
                }
            """,
            'variables': {
                'where': {
                    'workspaceId': self.workspaceId
                }
            }
        }
    def list(self):
        return self.request.post(self.getPayload()).get('sqls')
    def get(self, name):
        queries = self.list()
        query = next(q for q in queries if q.get('title') == name)
        return  query

