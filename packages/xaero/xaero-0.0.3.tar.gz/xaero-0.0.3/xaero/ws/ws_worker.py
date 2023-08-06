import uuid
import json
import asyncio
from urllib.parse import urlparse

from autobahn.asyncio.websocket import WebSocketClientFactory, WebSocketClientProtocol

from ..charger import Charger
from ..ocpp15.base import OcppMessage, OcppProtocolException, OcppError
from ..time_tools import Timeout


OCPP_J_CALL = 2        # Client-to-Server
OCPP_J_CALLRESULT = 3  # Server-to-Client
OCPP_J_CALLERROR = 4   # Server-to-Client

class MyClientProtocol(WebSocketClientProtocol):
    Charger = None
    Log = None
    Loop = None

    def onOpen(self):
        self.Log.info ('WebSocket connection open')
        
        self._last_request = None   # (id, action, timeout, callback)

        self.Loop.call_later(1.0, self.onTimer)

    def onMessage(self, payload, isBinary):
        assert not isBinary

        log = self.Log
        
        msg = None
        try:
            msg = json.loads(payload.decode('utf8'))
            
            log.debug('Message from CS: %s', msg)
            
            if msg[0] == OCPP_J_CALL:
                _, req_id, req_action, req_payload = msg

                log.info('CALL from CS: %s %s', req_action, req_payload)
                
                try:
                    resp_payload = self.Charger.on_request_from_cs(req_action, req_payload)
                    assert isinstance(resp_payload, dict), resp_payload
                    
                    log.info('Response to CS: %s', resp_payload)

                    ws_msg = [OCPP_J_CALLRESULT, req_id, resp_payload]
                
                except OcppError as ocpp_err:
                    log.error('Error processing request %s: %s', msg, str(ocpp_err))
                    ws_msg = [OCPP_J_CALLERROR, req_id, ocpp_err.ErrorCode.value, str(ocpp_err), {}]
                
                log.debug('Response to CS: %s', ws_msg)                
                self.sendMessage(json.dumps(ws_msg).encode('utf8'))
                
            elif msg[0] == OCPP_J_CALLRESULT:

                _, resp_id, resp_payload = msg

                log.info('CALLRESULT from CS: %s', resp_payload)

                if self._last_request:
                    req_id, req_action, _, cb = self._last_request
                    
                    if resp_id != req_id:
                        raise OcppProtocolException(f'Request/response mismatch (probably timeout)')

                    self._last_request = None
                    if cb:
                        cb(resp_payload)
                else:
                    raise OcppProtocolException(f'Unexpected response (probably timeout)')
                    
            elif msg[0] == OCPP_J_CALLERROR:
                log.error('CALLERROR from CS: %s', msg)
            else:
                raise OcppProtocolException(f'Message type "{msg[0]}" unknown')
        
        except Exception as ex:
            log.error(msg)
            raise
        
    def onTimer(self):
        self.Loop.call_later(1.0, self.onTimer)

        log = self.Log
        
        if self._last_request:
            _, action, timeout, cb = self._last_request
            if timeout.is_expired():
                log.error('Timeout on request to CS %s', action)
                if cb:
                    cb(None)
                self._last_request = None   
            else:
                return
        
        assert not self._last_request
        
        tpl = self.Charger.get_request_to_cs()
        if tpl:
            action, payload, cb = tpl
            id = str(uuid.uuid4())
            
            self._last_request = (id, action, Timeout(5.0), cb)
            
            request_json = [OCPP_J_CALL, id, action, payload]

            log.info('Request to CS: %s %s', action, payload)
            log.debug('Request to CS: %s', request_json)
            
            self.sendMessage(json.dumps(request_json).encode('utf8'))

    def onClose(self, wasClean, code, reason):
        self.Log.error ('WebSocket connection closed. Code=%s; Reason=%s', code, reason)
        self.Loop.stop()

'''    
def test_con(env, charger_info, log):
    import socket
    import select

    url = charger_info.CentralStationAddress

    log.info(f'Test connection to {url}...')

    url_items = urlparse(url)    
    host = url_items.hostname
    port = url_items.port or 80
    path = url_items.path + '/' + charger_info.Id

    s = None
    try:
        log.info(f'1. Open raw connection to {host}:{port}')
        s = socket.create_connection((host, port), timeout=5.0)

        log.info(f'2. Send HTTP request GET {path}')
        req_lines = [
            f'GET {path} HTTP/1.1',
            'User-Agent: tiger',
            f'Host: {host}:{port}',
            'Upgrade: WebSocket',
            'Connection: Upgrade',
            'Pragma: no-cache',
            'Cache-Control: no-cache',
            'Sec-WebSocket-Key: omf+YISYGBBTwPNsGSiWtg==',
            'Sec-WebSocket-Protocol: ocpp1.5',
            'Sec-WebSocket-Version: 13',
            '\r\n',
        ]
        s.sendall('\r\n'.join(req_lines).encode('utf-8'))
    
        fd_read, fd_write, fd_err = select.select([s], [], [], 5.0)
        if s in fd_read:
            data = s.recv(1024)
            if data:
                log.info(data)
            else:
                raise Exception('Socket closed while reading')
        else:
            raise Exception('Timeout reading')
    
    
    except Exception as ex:
        log.error(ex)

    finally:
        try:
            if s: s.close()
            s = None
        except:
            pass
'''

def websocket_run(env, charger_info, config, log):
    #test_con(env, charger_info, log)

    ws_url = charger_info.CentralStationAddress
    if ws_url.endswith('/'):
        ws_url += charger_info.Id
    else:
        ws_url += '/' + charger_info.Id
    
    ws_url_items = urlparse(ws_url)

    my_charger = Charger(charger_info)
    
    log.info(f'WebSocket endpoint: {ws_url}')
    factory = WebSocketClientFactory(url=ws_url, protocols=['ocpp1.5'])
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()

    MyClientProtocol.Charger = my_charger
    MyClientProtocol.Log = log
    MyClientProtocol.Loop = loop
    
    coro = loop.create_connection(factory, ws_url_items.hostname, ws_url_items.port or 80)
    try:
        try:
            loop.run_until_complete(coro)
        except (TimeoutError, ConnectionRefusedError) as ex:
            log.error(ex)
            return 1
            
        loop.run_forever()
        return 0
    finally:
        loop.close()     
        