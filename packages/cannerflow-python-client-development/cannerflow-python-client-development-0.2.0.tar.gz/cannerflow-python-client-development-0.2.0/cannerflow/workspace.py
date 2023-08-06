from cannerflow.request import Request
from cannerflow.saved_query import SavedQuery
from cannerflow.statement import Statement

__all__ = ["Workspace"]

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
        request = Request(
            headers=headers,
            endpoint=endpoint
        )
        self.request = request
        self.saved_query = SavedQuery(
            request=request,
            workspaceId=workspaceId
        )
        self.statement = Statement(
            request=request,
            workspaceId=workspaceId
        )