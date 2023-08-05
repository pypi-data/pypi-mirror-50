import datetime

from .ocpp15.types import OcppErrorCode
from .ocpp15.base import OcppError
from .constraints import CONSTRAINTS


class MsgReader:
    def __init__(self, action: (str, None), payload: dict, charger_info, log):
        assert action is None or isinstance(action, str), action
        assert isinstance(payload, dict), payload

        self._action = action
        self._payload = payload
        self._charger_info = charger_info
        self.log = log

    def str(self, name: str, max_len: int = None, def_val=None):
        assert name and isinstance(name, str), name

        if name not in self._payload:
            if def_val is None:
                raise OcppError(f'Missing "{name}" in payload {self._payload}', OcppErrorCode.PropertyConstraintViolation)
            return def_val
            
        v = self._payload[name]
        if max_len and len(v) > max_len:
            raise OcppError(f'Field "{name}={v}" in payload {self._payload} violates max length {max_len} (it is {len(v)} chars).', OcppErrorCode.PropertyConstraintViolation)

        return v

    def int(self, name: str, def_val=None):
        assert name and isinstance(name, str), name
        
        if name not in self._payload:
            if def_val is None:
                raise OcppError(f'Missing "{name}" in payload {self._payload}', OcppErrorCode.PropertyConstraintViolation)
            return def_val
            
        v = self._payload[name]
        try:
            return int(v)
        except ValueError:
            raise OcppError(f'Field "{name}={v}" in payload {self._payload} is invalid integer.', OcppErrorCode.PropertyConstraintViolation)

    def dtm(self, name: str, def_val=None):
        assert name and isinstance(name, str), name

        if name not in self._payload:
            if def_val is None:
                raise OcppError(f'Missing "{name}" in payload {self._payload}', OcppErrorCode.PropertyConstraintViolation)
            return def_val
            
        v = self._payload[name]
        try:
            return datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')    # %f is microsec, xxxxxx
            #return datetime.datetime.fromisoformat(v)  # from Python 3.7
        except ValueError as ex:
            pass
            
        # один лишний символ в мс
        v = v[:-2] + 'Z'
        try:
            res = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')    # %f is microsec, xxxxxx
            if 'cn.zaria.timestamp' not in self._charger_info.CloudInfo['constraints']:
                self.log.warn('DateTime is malformed. Use "cn.zaria.timestamp" constraint to supress this warning')
            return res
        except ValueError as ex:
            raise OcppError(f'Field "{name}={v}" in payload {self._payload} is invalid DATE: {ex}', OcppErrorCode.PropertyConstraintViolation)
 

    def enum(self, name: str, cls=None, def_val=None):
        assert name and isinstance(name, str), name

        if name not in self._payload:
            if def_val is None:
                raise OcppError(f'Missing "{name}" in payload {self._payload}', OcppErrorCode.PropertyConstraintViolation)
            return def_val
            
        v = self._payload[name]
        try:
            return cls(v)
        except ValueError:
            raise OcppError(f'Field "{name}={v}" in payload {self._payload} is invalid. Possible values: {list(cls.__members__)}', OcppErrorCode.PropertyConstraintViolation)
            
            
