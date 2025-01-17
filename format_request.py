from datetime import datetime
import utils
import bigquery

class FormatMessage:
    def __init__(self, data) -> None:
        self.contact_name = data.get('chatName') if data.get('chatName') else '?'
        self.user_name = data.get('senderName') if data.get('senderName') else '?'
        self.client_phone = data.get('phone') if data.get('phone') else '?'
        self.owner_phone = data.get('connectedPhone') if data.get('connectedPhone') else '?'
        self.is_group = data.get('isGroup') if data.get('isGroup') != None else False
        self.from_client = not data.get('fromMe') if data.get('fromMe') != None else False
        self.message_time = data.get('momment') if data.get('momment') else datetime.now()
        self.message = data.get('text', {}).get('message', None)
        self.message_id = data.get('messageId', None)
        
    @property
    def client_id(self):
        return self.get_client_id()
        
    def message_fields(self):
        return {
            "contact_name":self.contact_name,
            "user_name":self.user_name,
            "client_phone":self.client_phone,
            "owner_phone":self.owner_phone,
            "is_group":self.is_group,
            "from_client":self.from_client,
            "message_time":self.message_time,
            "message":self.message,
            "message_id":self.message_id,
            "client_id":self.client_id
        }
        
    def get_client_id(self):
        bigquery_client = bigquery.BigQueryClient(
            table_id='adm-lake.Public.Cadastro de Clientes',
            dataset_id='adm-lake.Public'
        )
        clients = bigquery_client.get_all_clients()
        for client in clients:
            if self.client_match(client, self.client_phone):
                return client['Cod_Cliente']
        return None
    
    @classmethod
    def client_match(cls, client, client_phone):
        phones = [client['Des_Tel_Sponsor'], client['Des_Telefone_Financeiro'], client['Des_Tel_Key_User']]
        if all(phone is None for phone in phones):
            return
        for phone in phones:
            if phone and utils.is_phone_match(phone, client_phone[2:]):
                return client['Cod_Cliente']
        return
        
class FormatSessions:
    def __init__(self, data) -> None:
        self.status = data.get('type') if data.get('type') else '?'
        self.owner_phone = data.get('phone') if data.get('phone') else '?'
        self.intance_id = data.get('instanceId') if data.get('instanceId') else '?'
        self.momment = data.get('momment') if data.get('momment') else datetime.now()
        
    def session_fields(self):
        return {
            "status":self.status,
            "owner_phone":self.owner_phone,
            "intance_id":self.intance_id,
            "momment":self.momment
        }