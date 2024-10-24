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
        if errors == []:
            return
        print(f'Error in BigQuery: {errors}')
        return errors

    def insert_row_alert(self, row):
        if self.check_message_exists(row['message_id']):
            print(f"Message with ID {row['message_id']} already exists.")
            return
        
        errors = self.client.insert_rows_json(self.table_id, [row])
        if errors == []:
            return
        print(errors)
        return errors
    
    def check_message_exists(self, message_id):
        query = f"""
        SELECT COUNT(*) as count 
        FROM `{self.table_id}` 
        WHERE message_id = @message_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("message_id", "STRING", message_id)
            ]
        )
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        for row in results:
            return row.count > 0
        return False
    
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
            "message_content":data['message'],
            "message_id":data['message_id'],
        }
        return row
            
    def get_id(self):
        return int(time.time() * 1000) + random.randint(0, 99)
    
    def list_rows(self):
            query = f"""
            SELECT *
            FROM (
                SELECT *,
                    ROW_NUMBER() OVER (PARTITION BY client_phone ORDER BY message_time DESC) AS row_num
                FROM `{self.table_id}`
                WHERE message_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 48 HOUR)
                AND from_client = TRUE
                AND is_group = FALSE
            )
            WHERE row_num = 1
            """
            return self.run_query(query)
            
            
    def message_in_contact_window(self, client_phone, message_time, interval=3):
        print(message_time)
        query = f"""
        SELECT *
        FROM `{self.table_id}`
        WHERE client_phone = '{client_phone}'
        AND message_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {interval} HOUR)
        AND from_client = FALSE
        AND is_group = FALSE
        """
                
        return self.run_query(query)
            
    def run_query(self, query):
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            rows = [dict(row) for row in results]
            
            return rows
        except GoogleAPIError as e:
            print(f"Erro ao listar registros do BigQuery: {e}")
            return []
        except NotFound as e:
            print(f"Tabela não encontrada: {e}")
            return []
        except PermissionDenied as e:
            print(f"Permissão negada ao acessar os dados do BigQuery: {e}")
            return []
        except Forbidden as e:
            print(f"Acesso proibido ao BigQuery: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao listar registros: {e}")
            return []
    
    
    def get_alert_row(self, data):
        row = {
            "alert_id":self.get_id(),
            "alert_creation_date":utils.bigquery_now(),
            "alert_type":"Whatsapp",
            "owner_name":data['owner_phone'],
            "client_name":data['contact_name'],
            "client_phone":data['client_phone'],
            "message_time":utils.datetime_to_iso(data['message_time']),
            "alert_description":"Mensagem enviado pelo cliente está há mais de 24h sem retorno.",
            "trigger_event":"Registro de mensagem, fora de grupo, enviada pelo cliente sem retorno há mais de 24h",
            "message_content":data['message_content'],
            "message_id":data['message_id'],
        }
        return row