import datetime


Optional = True
Mandatory = False


BootNotificationReq = (
    ('chargeBoxSerialNumber',   Optional),
    ('chargePointModel',        Mandatory),
    ('chargePointSerialNumber', Optional),
    ('chargePointVendor',       Mandatory),
    ('firmwareVersion',         Optional),
    ('iccid',                   Optional),
    ('imsi',                    Optional),
    ('meterSerialNumber',       Optional),
    ('meterType',               Optional),
)


def utc_str() -> str:    
    return str(datetime.datetime.utcnow().isoformat(timespec='milliseconds')) + 'Z' # '2019-03-18T10:21:03.944Z'


class OcppMessage:
    def __init__(self, action: (str, None), payload: dict):
        assert isinstance(payload, dict), payload
        
        self.Action = action    # can be None
        self.MessageID = None
        self.Payload = payload
        
    def __str__(self):
        return f'OcppMessage<Action={self.Action} MessageID={self.MessageID} Payload={self.Payload}>'


class OcppException(UserWarning):
    def __init__(self, msg: str):
        super().__init__(msg)


class OcppProtocolException(OcppException):
    def __init__(self, msg: str):
        super().__init__(msg)


class OcppError(UserWarning):
    def __init__(self, msg: str, code):
        super().__init__(msg)
        self.ErrorCode = code

