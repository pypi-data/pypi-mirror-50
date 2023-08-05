from autologging import logged
import base64
import requests
import json
from concurrent.futures import ThreadPoolExecutor


@logged
class Client:
    def __init__(self, url, port, username, password):
        self.url = url
        self.port = port
        self.username = username
        self.password = password

        self.session = requests.Session()
        self.headers = {'Accept': 'application/json', 'Connection': 'keep-alive',
                        'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'en-US,en'}
        self.db_data = {}
        self.batch_queries = []
        self.batch_lists = []

    def connect(self):
        username = str(self.username).strip()
        password = str(self.password).strip()
        credentials = str(base64.b64encode(bytes(username + ':' + password, encoding='latin-1')), 'latin-1')
        headers = self.headers.copy()
        headers['Authorization'] = 'Basic ' + credentials

        url = '{}:{}/'.format(self.url, self.port) + '/'.join(['connect', self.db])
        try:
            connect_response = self.session.get(url, allow_redirects=False, headers=headers)
        except OSError:
            raise ConnectionError("Check url, https flag")
        if connect_response.status_code == 204:
            message = {'url_path': ['database', self.db]}
            self.db_data = json.loads(self.get(**message).text)
        elif connect_response.status_code == 401:
            raise Exception('OrientDB credentials or db_name is wrong')
        self.__log.debug("Connected to DB successfully")
        return True

    def send_vertexes(self, vertexes):
        pass

    def send_edges(self, edges):
        pass

    def add_query(self, query):  # TODO : this part is probably critical section and we maybe need to use lock here
        self.batch_queries.append(query)
        # if len(self.batch_queries) > 2000:  # TODO : need to get this value from the config
        #     self.send_batch_query()
        #     self.batch_queries = []

    def send_batch_query(self):
        q_list = []
        for i, val in enumerate(self.batch_queries):
            q_list.append(val)
            if len(q_list) > 500:
                batch_query_string = ";".join(q_list)
                query = "BEGIN;{};COMMIT RETRY 100;".format(batch_query_string)
                self.batch_lists.append(query)
                q_list = []
        batch_query_string = ";".join(q_list)
        query = "BEGIN;{};COMMIT;".format(batch_query_string)
        self.batch_lists.append(query)
        with ThreadPoolExecutor(max_workers=1) as executor:
            for _ in executor.map(self.handle_batch, self.batch_lists):
                pass

    def close(self):
        if self.session:
            self.session.close()
