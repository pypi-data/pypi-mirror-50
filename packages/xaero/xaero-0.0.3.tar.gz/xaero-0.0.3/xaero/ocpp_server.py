import sys
import argparse
import logging
import json

from .mylog import configure_arg_parser_for_log, configure_logger
from .client_websocket import websocket_run
from .client_soap import soap_run
from .charger import ChargerInfo

'''
class OcppServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        req = parse_req(body)
        
        print(req)
        
        if req.Action == 'BootNotification':
            res_payload = {
                'status': 'Accepted',
                'currentTime': _current_time_utc(),
                'heartbeatInterval': 5000
            }
            
        elif req.Action == 'StatusNotification':
            res_payload = {
            }          
            
        elif req.Action == 'Heartbeat':
            res_payload = {
                'currentTime': _current_time_utc(),
            }          
            
        elif req.Action == 'Authorize':
            res_payload = {
                'idTagInfo': {
                    'status': 'Accepted'
                }
            }          
            
        else:
            print ('Error', self.path, body)
            raise Exception (f'Unknown action: {req.Action}')
            
        res_bytes = build_res(req, req.Action + 'Response', res_payload)
        self.send_response(200)
        self.send_header('Content-type', 'application/soap+xml; charset=utf-8;')
        self.end_headers()
        self.wfile.write(res_bytes)
'''
