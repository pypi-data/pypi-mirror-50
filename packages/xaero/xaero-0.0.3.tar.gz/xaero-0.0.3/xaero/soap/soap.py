

def lcamel(s: str) -> str:
    assert isinstance(s, str), s
    return s[0].lower() + s[1:]
    
    
def ucamel(s: str) -> str:
    assert isinstance(s, str), s
    return s[0].upper() + s[1:]


class SoapException(UserWarning):
    def __init__(self, msg: str):
        super().__init__(msg)
    
FAULT_ACTION = 'urn://Ocpp/Cs/2012/06/:CentralSystemService:StatusNotification:Fault:SoapFault'
FAULT_PAYLOAD_NODE_NAME = 'Fault'
    
def is_fault_action(action:str) -> bool:
    return action == FAULT_ACTION


def fqid(id: str) -> str:
    return 'urn:uuid:' + id


def unqualify_id(id: str) -> str:
    return id[len('urn:uuid:'):] if id.startswith('urn:uuid:') else id


def create_fault_msg(code: str, subcode: str, reason: str):
    payload = {
        'Code':{
            'Value': code,
            'Subcode':{
                'Value': subcode
            }
        },
        'Reason':{
            'Text': reason
        }
    }
    return SoapMessage(FAULT_ACTION, payload)

class SoapMessage:
    def __init__(self, action: (str, None), payload: dict):
        assert action is None or isinstance(action, str), action
        assert isinstance(payload, dict), payload
        
        self.Action = action
        self.MessageID = None
        self.ChargeBoxIdentity = None
        self.RelatesTo = None
        self.ChargerPublicAddress = None
        self.CentralStationAddress = None
        self.Payload = payload
        
        
    def is_fault(self):
        return is_fault_action(self.Action)
        
    def fault_text(self) -> str:
        assert self.is_fault(), self
        assert self.Payload, self
        assert 'Reason' in self.Payload, self
        assert 'Text' in self.Payload['Reason'], self
        
        return self.Payload['Reason']['Text']
        
    def __str__(self):
        return f'SoapMessage<Action={self.Action} MessageID={self.MessageID} ChargeBoxIdentity={self.ChargeBoxIdentity} RelatesTo={self.RelatesTo} ChargerPublicAddress={self.ChargerPublicAddress} CentralStationAddress={self.CentralStationAddress} Payload={self.Payload}>'

