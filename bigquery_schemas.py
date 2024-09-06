from google.cloud import bigquery

class BigQuerySchemas:
    def message_schema(cls):
        schema = [
            bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("from_client", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("message_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("is_group", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("owner_phone", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("client_phone", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("user_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("contact_name", "STRING", mode="NULLABLE"),
        ]
        
        return schema