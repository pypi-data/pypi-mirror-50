import requests
import json
import time

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

from ..ocpp15.base import OcppMessage, OcppProtocolException, OcppError
from ..charger import Charger
from .soap import SoapMessage, create_fault_msg
from .soap_build import build_msg
from .soap_parse import parse_message

MIME={}
MIME['txt'] = 'text/plain; charset=utf-8'
MIME['html'] = 'text/html; charset=utf-8'
MIME['css'] = 'text/css'
MIME['js'] = 'application/javascript'
MIME['jpg'] = 'image/jpg'
MIME['json'] = 'application/json'
MIME['xml'] = 'application/xml; charset=utf-8'


def soap_request(req: SoapMessage, log) -> SoapMessage:
    assert isinstance(req, SoapMessage), req
    assert req.Action, req
    assert isinstance(req.Payload, dict), req   # empty {} is False
    
    log.info('Request to CS: %s %s', req.Action, req.Payload)
    
    #log.debug('Request to CS: %s', req)

    req_bytes = build_msg(req, is_request=True)

    log.debug('CP ==(req)=> CS: %s', req_bytes)
    
    # raises
    resp_http = requests.post(req.CentralStationAddress, data=req_bytes)
    
    log.debug('Response %s %s %s', resp_http.status_code, resp_http.headers, resp_http.content)
    
    resp = parse_message(resp_http.content, is_request=False)
        
    log.info('Response from CS: %s %s', resp.Action, resp.Payload)
    log.debug('Response from CS: %s', resp)
            
    # Check for faults
    if resp.is_fault():
        raise Exception(f'Fault for request {req}: {resp.fault_text()}')

    #expected_resp_action = req.Action + 'Response'
    #if resp.Action != expected_resp_action:
    #    raise Exception(f'Request/response mismatch. Expected response action {expected_resp_action} but got {resp.Action}. Response: {resp}')
        
    if resp.RelatesTo != req.MessageID:
        raise Exception(f'Request/response mismatch. Expected response RelatesTo={req.MessageID} but got  {resp.RelatesTo}. Response: {resp}')
        
    return resp


class WebInterfaceHttpServer(http.server.BaseHTTPRequestHandler):
    Charger = None
    Config = None
    Log = None
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        
        url = urlparse(self.path)
        q = parse_qs(url.query)
        
        if url.path == '/control/authorize':
            self.Charger.manual_Authorize(q['idTag'][0])
            self.send_response(204)
            self.end_headers()
        elif url.path == '/monitor/tags':
            self.send_response(200)
            self.send_header('Content-type', MIME['json'])
            self.end_headers()
            self.wfile.write(json.dumps(self.Config['tags']).encode())
        else:
            dot = url.path.rfind('.')
            if dot != -1:
                ext = url.path[dot+1:]
                self.sendFile('./www/' + url.path, MIME.get(ext, MIME['txt']))
            else:
                self.sendFile('./www/' + url.path, MIME['txt'])
   
    def sendFile(self, path, mime):
        try:
            with open(path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', mime)
                self.end_headers()
                self.wfile.write(f.read())
        except IOError as ex:
            self.send_error(404, f'Error reading {path}: {ex}')
            
            
class SoapChargerServer(http.server.BaseHTTPRequestHandler):
    Charger = None
    Log = None

    '''
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        
        url = urlparse(self.path)
        print (url.path)
        
        if url.path == '/control/authorize':
            self.Charger.postpone_authorize('17171771771')
            self.send_response(204)
            self.end_headers()
        else:
            dot = url.path.rfind('.')
            if dot != -1:
                ext = url.path[dot+1:]
                self.sendFile('./www/' + url.path, MIME.get(ext, MIME['txt']))
            else:
                self.sendFile('./www/' + url.path, MIME['txt'])
    '''    
    def do_POST(self):
        log = self.Log
        
        if self.path != '/':
            raise Exception(f'POST is only accepted on path "/", not "{self.path}"')
        
        content_len = int(self.headers.get('Content-Length', 0))
        body: bytes = self.rfile.read(content_len)
        req: SoapMessage = parse_message(body, is_request=True)

        log.info('Request from CS: %s %s', req.Action, req.Payload)
        log.debug('Request from CS: %s', req)

        try:
            resp_payload = self.Charger.on_request_from_cs(req.Action, req.Payload)
            
            resp = SoapMessage(req.Action + 'Response', resp_payload)
        except OcppError as ocpp_err:
            log.error('Error processing request %s: %s', req, str(ocpp_err))
            resp = create_fault_msg(ocpp_err.ErrorCode.value, 'SecurityError', str(ocpp_err))
        
        resp.ChargeBoxIdentity = self.Charger.Info.Id
        resp.RelatesTo = req.MessageID
        resp.ChargerPublicAddress = ''
        resp.CentralStationAddress = self.Charger.Info.CentralStationAddress

        log.info('Response to CS: %s %s', resp.Action, resp.Payload)
        
        resp_xml = build_msg(resp, is_request=False)
        log.debug('CP ==(resp)=> CS: %s', resp_xml)

        self.send_response(200)
        self.send_header('Content-type', MIME['xml'])
        self.end_headers()
        self.wfile.write(resp_xml)


class BothServers(WebInterfaceHttpServer, SoapChargerServer):
    pass

def run_charger_once(charger, log):
    """
        Обрабатывает выходные запросы от ЗС
    """
    tpl = charger.get_request_to_cs()
    if not tpl:
        return
        
    action, payload, cb = tpl
    
    msg = SoapMessage(action, payload)
    msg.ChargeBoxIdentity = charger.Info.Id
    msg.ChargerPublicAddress = charger.Info.ChargerPublicAddress
    msg.CentralStationAddress = charger.Info.CentralStationAddress

    resp = soap_request(msg, log)
    
    if cb:
        cb(resp.Payload)
    else:
        log.debug('Response ignored - no callback specified')

def soap_run(env, charger_info, config, log):
    if not charger_info.ChargerPublicAddress:
        log.warn ('Public address not specified, SOAP reverse commands wont work. Use --public "http://1.2.3.4:5678" argument')

    my_charger = Charger(charger_info)

    SoapChargerServer.Charger = my_charger
    SoapChargerServer.Log = log
    
    WebInterfaceHttpServer.Charger = my_charger
    WebInterfaceHttpServer.Config = config
    WebInterfaceHttpServer.Log = log
    
    log.info(f'SOAP Endpoint is {charger_info.CentralStationAddress}')
    
    # Сервер запускается если указан обратный адрес подключения к ЗС или нужен веб-интерфейс для управления
    if charger_info.ChargerPublicAddress or env.web:
        if env.port:
            port = env.port
            log.info(f'Listening on explicitly specified port {port}')
        else:
            # Если порт не указан явно, попытаемся получить его из публичного адреса
            port = None
            if charger_info.ChargerPublicAddress:
                url = urlparse(charger_info.ChargerPublicAddress)
                if url.port:
                    port = url.port
                    log.info(f'Listening on port {port} from public url {charger_info.ChargerPublicAddress}')
            
            if not port:
                port = 80
                log.info(f'Listening on default port {port}. Use --port option to change it')
            
        server_type = None
        if charger_info.ChargerPublicAddress and env.web:
            server_type = BothServers
        elif charger_info.ChargerPublicAddress:
            server_type = SoapChargerServer
        else:
            server_type = WebInterfaceHttpServer
            
        with socketserver.TCPServer(('', port), server_type) as httpd:
            #httpd.serve_forever()
            httpd.timeout = 0.5
            while True:
                httpd.handle_request()
                run_charger_once(my_charger, log)
    else:
        log.info('No HTTP server is setup - charger has no public address and web interface was not requested')
        while True:
            run_charger_once(my_charger, log)
            time.sleep(0.2)
    
    return 0