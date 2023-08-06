import sys
import argparse
import logging

from .mylog import configure_arg_parser_for_log, configure_logger
from .ws.ws_worker import websocket_run
from .soap.soap_worker import soap_run
from .test_conn import test_con
from .charger import ChargerInfo
from .constraints import CONSTRAINTS
from .config import CONFIG

def main():
    parser = argparse.ArgumentParser()
    configure_arg_parser_for_log(parser)
    parser.add_argument('--cloud', help='Cloud', default='default')
    parser.add_argument('--charger', help='Charger')
    parser.add_argument('--port', help='Server TCP/IP port', type=int)
    parser.add_argument('--server', help='Enable Server mode', action='store_true')
    parser.add_argument('--public', help='Public address of current station')
    parser.add_argument('--soap', help='Enable SOAP mode', action='store_true')
    parser.add_argument('--ws', help='Enable WebSocket mode', action='store_true')
    parser.add_argument('--web', help='Enable web interface', action='store_true')
    parser.add_argument('--test', help='Test connection', action='store_true')
    parser.add_argument('--id', help='Override charger id')
    env = parser.parse_args()

    # Logging
    configure_logger(env)
    log = logging.getLogger()

    # Arguments
    try:
        if env.soap and env.ws:
            raise UserWarning('You cannot combine WebSocket and SOAP modes')
            
    except UserWarning as ex:
        log.error(ex)
        return 1
        

    # Config
    config = CONFIG
    
    try:
        # Cloud
        clouds = config.get('clouds')
        if not clouds:
            raise UserWarning('Invalid config: element "clouds" not found')
            
        if env.cloud.startswith('ws:'):
            cloud_info = {
                'ws': env.cloud,
                'constraints':[]
            }
            env.soap = False
            log.info('Set WebSocket custom enpoint: %s', env.cloud)
        elif env.cloud.startswith('http:') or env.cloud.startswith('https:'):
            cloud_info = {
                'soap': env.cloud,
                'constraints':[]
            }
            env.soap = True
            log.info('Set SOAP custom enpoint: %s', env.cloud)
        else:
            cloud_info = clouds.get(env.cloud)
            if not cloud_info:
                raise UserWarning(f'Cloud "{env.cloud}" does not exist. Available: {list(clouds.keys())}')
            log.info('Selected cloud: %s', env.cloud)
        
        # if user didnt select explicitly
        if not env.soap and not env.ws:
            if cloud_info.get('ws'):  # if cloud supports websockets
                log.info('Implicitly selected WebSocket mode for cloud')
                env.soap = False
            else:
                log.info('Implicitly selected SOAP mode for cloud')
                env.soap = True
        
        # Check cloud constraints
        for cl_name, cl_data in clouds.items():
            if isinstance(cl_data, dict):    # skip "default": "foo"
                if 'constraints' in cl_data:
                    for c in cl_data['constraints']:
                        if not c in CONSTRAINTS:
                            raise UserWarning(f'Unknown constraint "{c}" in cloud "{cl_name}". Known constraints: {list(CONSTRAINTS.keys())}')
                else:
                    cl_data['constraints'] = []
                
                
        # Charger
        chargers = config.get('chargers')
        hardware = config.get('hardware')
        if not chargers:
            raise UserWarning('Invalid config: element "chargers" not found')
        if not hardware:
            raise UserWarning('Invalid config: element "hardware" not found')
        
        charger_helper = list(chargers.keys()) + list(hardware.keys())
        
        if env.charger:
            charger_info = chargers.get(env.charger)
            if not charger_info:
                hw = hardware.get(env.charger)
                if not hw:
                    raise UserWarning(f'Charger "{env.charger}" does not exist. Available: {charger_helper}')
                charger_info = {
                  "id": env.id or "foo",
                  "model": env.charger,
                  "meta": {}
                }
            log.info('Selected charger: %s', env.charger)
        else:
            charger_info = chargers.get('default')
            if not charger_info:
                raise UserWarning(f'There is not default charger specified. Use --charger with values {charger_helper}')
            log.info('Selected charger: %s', 'default')
                
        ch_model = hardware[charger_info['model']]
        
        # Merge meta from charger instance and model
        all_meta = charger_info['meta']
        for k, v in ch_model['meta'].items():
            if k not in all_meta:
                all_meta[k] = v
            
        final_id = env.id or charger_info['id']
        
        if env.soap:
            my_charger_info = ChargerInfo(final_id, cloud_info['soap'], env.public, ch_model['nbConnectors'], all_meta, cloud_info)
            return test_con(env, my_charger_info, log) if env.test else soap_run(env, my_charger_info, config, log)
        else:
            my_charger_info = ChargerInfo(final_id, cloud_info['ws'], None, ch_model['nbConnectors'], all_meta, cloud_info)
            return test_con(env, my_charger_info, log) if env.test else websocket_run(env, my_charger_info, config, log)
        
    except UserWarning as ex:
        log.error(ex)
        return 1

    return 0

sys.exit(main())
