import os
import json
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError, NotFound, PermissionDenied, Forbidden
import utils
import time
import random

class BigQueryClient:
    def __init__(self, table_id, dataset_id) -> None:
        self.client = self.get_client()
        self.table_id = table_id
        self.dataset_id = dataset_id
    
    def get_client(self):
        try:
            client = bigquery.Client.from_service_account_json('./adm-lake-1cfeab192f2e.json')

            datasets = list(client.list_datasets())
            if datasets:
                pass
            else:
                return
        except GoogleAPIError as e:
            print(f"Erro ao conectar ao BigQuery: {e}")
            return
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return

        return client

    def insert_row(self, data):
        row = [self.get_row(data)]
        errors = self.client.insert_rows_json(self.table_id, row)
        print(errors)
        if errors == []:
            return
        return errors
    
    def get_row(self, data):
        row = {
            "id":self.get_id(),
            "from_client":data['from_client'],
            "message_time":utils.convert_time_bigquery(data['message_time']),
            "is_group":data['is_group'],
            "owner_phone":data['owner_phone'],
            "client_phone":data['client_phone'],
            "user_name":data['user_name'],
            "contact_name":data['contact_name'],
        }
        return row
            
    def get_id(self):
        return int(time.time() * 1000) + random.randint(0, 99)
            