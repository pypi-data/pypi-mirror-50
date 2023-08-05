import json

import base64 import base64
import gzip	import gzip
import threading
from autologging import logged
from logger.logger import logger
from ..common.client import Client as TemplateClient
from ..encoder import JSONDefaultEncoder
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


class Test:
    def create_vertex_with_edge(self, anchor_cluster_name, anchor_filter, data_cluster_name, data, data_filter):
        anchor_rid = self.get_rid(anchor_cluster_name, anchor_filter)  # TODO : need to add debugging messages + retry
        data_rid = self.write_to_channel(data_cluster_name, data, data_filter)
        data_create_query = "INSERT INTO {} content {}".format(data_cluster_name,
                                                               self._prepare_message(data))
        # build the anchor and data queries
        data_query = "SELECT * from {} where {}='{}'".format(data_cluster_name, data_filter['filter_by'],
                                                             data[data_filter['filter_by']])

        filter_and_create_vertex_query = f"let $a={data_query};if($a.size()==0){'{let $b=' + data_create_query + ';}'}"

        anchor_filter = anchor_filter.popitem()


        anchor_filter_by = anchor_filter[0]
        anchor_filter_value = anchor_filter[1]
        anchor_query = "SELECT * from {} where {}='{}'".format(anchor_cluster_name, anchor_filter_by,
                                                               anchor_filter_value)

        # create edge and prevent duplicates
        data_rid_query = "SELECT @rid from {} where {}='{}'".format(data_cluster_name, data_filter['filter_by'],
                                                                    data[data_filter['filter_by']])
        anchor_rid_query = "SELECT @rid from {} where {}='{}'".format(anchor_cluster_name, anchor_filter_by,
                                                                      anchor_filter_value)

        is_edge_exist_query = f"select * from E where out in ({data_rid_query}) and in in ({anchor_rid_query})"

        create_edge_query = f"CREATE EDGE E from ({anchor_query}) to ({data_query}) RETRY 100"
        filter_and_create_edge_query = f"let $a={is_edge_exist_query};" \
                                       f"if($a.size()==0){'{let $b=' + create_edge_query + ';}'}"

        self.add_query(filter_and_create_vertex_query)
        self.add_query(filter_and_create_edge_query)


    def create_edge_by_fingerprints(self, source_fingerprint, dest_fingerprint, source_cluster='V', dest_cluster='V',
                                    edge_type='function'):
        # build the queries for the 2 nodes
        source_query = f"SELECT * from {source_cluster} where fingerprint ='{source_fingerprint}'"
        source_query_rid = f"SELECT @rid from {source_cluster} where fingerprint ='{source_fingerprint}'"
        dest_query = f"SELECT * from {dest_cluster} where fingerprint ='{dest_fingerprint}'"
        dest_query_rid = f"SELECT @rid from {dest_cluster} where fingerprint ='{dest_fingerprint}'"

        # create edge and prevent duplicates
        is_edge_exist_query = f"select * from {edge_type} where out in ({source_query_rid})" \
                              f" and in in ({dest_query_rid})"
        create_edge_query = f"CREATE EDGE {edge_type} from ({source_query}) to ({dest_query}) RETRY 100"
        filter_and_create_edge_query = f"let $a={is_edge_exist_query}" \
                                       f";if($a.size()==0){'{let $b=' + create_edge_query + ';}'}"
        # create edge and prevent duplicates
        self.add_query(filter_and_create_edge_query)

    def batch_sql(self, sql_script, session):
        # TODO : need to refactor this part to save duplication of code
        # TODO : need to add retries + catch of exceptions + other like _send function
        username = str(self.config.ORIENTDB_DB_USERNAME).strip()
        password = str(self.config.ORIENTDB_DB_PASSWORD).strip()
        credentials = str(base64.b64encode(bytes(username + ':' + password, encoding='latin-1')), 'latin-1')
        headers = self.headers.copy()
        headers['Authorization'] = 'Basic ' + credentials
        url = '{}:{}/'.format(self.url, self.port) + 'batch/' + self.db  # The format for url batch
        body = {"transaction": False,
                "operations": [
                    {
                        "type": "script",
                        "language": "sql",
                        "script": [sql_script]
                    }
                ]
                }
        json_data = json.dumps(body, cls=JSONDefaultEncoder)
        gzip_data = gzip.compress(json_data.strip().encode('utf8'))
        headers['Content-Length'] = str(len(gzip_data))
        headers['Accept-Encoding'] = 'gzip'
        params = {}

        res = session.post(url, allow_redirects=False, headers=headers, params=params,
                           data=gzip_data)

        self.__log.debug("Response from db: {}".format(res.content))

    def add_query(self, query):  # TODO : this part is probably critical section and we maybe need to use lock here
        with self.lock:
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
        with PoolExecutor(max_workers=1) as executor:
            for _ in executor.map(self.handle_batch, self.batch_lists):
                pass

    def handle_batch(self, query):
        print("handle batch")
        s = requests.Session()
        self.batch_sql(query, s)