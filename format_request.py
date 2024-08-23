class FormatMessage:
    def __init__(self, data) -> None:
        self.contact_name = data.get('chatName')
        self.user_name = data.get('senderName')
        self.client_phone = data.get('phone')
        self.owner_phone = data.get('connectedPhone')
        self.is_group = data.get('isGroup')
        self.message_time = data.get('momment')
        
    def message_fields(self):
        return {
            "contact_name":self.contact_name,
            "user_name":self.user_name,
            "client_phone":self.client_phone,
            "owner_phone":self.owner_phone,
            "is_group":self.is_group,
            "message_time":self.message_time,
        }