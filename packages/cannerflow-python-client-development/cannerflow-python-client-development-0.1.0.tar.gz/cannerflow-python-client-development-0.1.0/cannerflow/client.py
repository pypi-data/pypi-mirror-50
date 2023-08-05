# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cannerflow.workspace
import cannerflow.dbapi
from cannerflow import constants, exceptions
from cannerflow.transaction import Transaction, IsolationLevel, NO_TRANSACTION

__all__ = ["bootstrap", "Client"]

def bootstrap(*args, **kwargs):
    return Client(*args, **kwargs)

class Client(object):
    def __init__(self,
        host,
        application_endpoint,
        token,
        workspaceId,
        port=constants.DEFAULT_PORT,
        user=None,
        source=constants.DEFAULT_SOURCE,
        catalog=constants.DEFAULT_CATALOG,
        schema=constants.DEFAULT_SCHEMA,
        session_properties=None,
        http_headers=None,
        http_scheme=constants.HTTP,
        auth=constants.DEFAULT_AUTH,
        redirect_handler=cannerflow.redirect.GatewayRedirectHandler(),
        max_attempts=constants.DEFAULT_MAX_ATTEMPTS,
        request_timeout=constants.DEFAULT_REQUEST_TIMEOUT,
        isolation_level=IsolationLevel.AUTOCOMMIT
    ):
        self.connection = cannerflow.dbapi.connect(
            host,
            port,
            user,
            source,
            catalog,
            schema,
            session_properties,
            http_headers,
            http_scheme,
            auth,
            redirect_handler,
            max_attempts,
            request_timeout,
            isolation_level
        )
        self.workspace = cannerflow.workspace.Workspace(
            endpoint=application_endpoint,
            headers={
                "Authorization": f"Bearer {token}"
            },
            workspaceId=workspaceId
        )
    def useSavedQuery(self, name):
        query = self.workspace.savedQuery.get(name)
        return self.execute(query['sql'])
    def listSavedQuery(self):
        return self.workspace.savedQuery.list()
    def execute(self, sql):
        cur = self.connection.cursor()
        cur.execute(sql)
        return cur
