import xml.etree.ElementTree as ET

from .soap import SoapMessage, lcamel, ucamel, SoapException, is_fault_action, unqualify_id


def _local_name(name: str) -> str:
    """
    Removes namespace from node name
    """
    assert name and isinstance(name, str), name
    
    return name.split('}')[1] if '}' in name else name


def _get_xml_node(root, path: str):
    """
        Throws SoapException
        
        path: a/b/c
    """
    assert path and isinstance(path, str), path

    res = root
    for short_name in path.split('/'):
        found = False
        for ch_node in res:
            if _local_name(ch_node.tag) == short_name:
                found = True
                res = ch_node
                break
        if not found:
            raise SoapException(f'Path "{path}" could not be resolved, stopped on "{short_name}"')
    return res


def _parse_payload(payload_node) -> dict:
    res = {}
    for nd in payload_node:
        nd_name = _local_name(nd.tag)
        if list(nd):  # has subnodes?
            res[nd_name] = _parse_payload(nd)
        else:
            res[nd_name] = nd.text
            
    return res
    
    
def _t(root, path: str) -> str:
    return _get_xml_node(root, path).text
        
    
def parse_message(xml_data: bytes, is_request: bool) -> SoapMessage: 
    try:
        root = ET.fromstring(xml_data)
    except Exception as ex:
        raise SoapException(f'Malformed XML data: {xml_data}')
    

    action = _t(root, 'Header/Action')

    if is_request:
        if not action.startswith('/'):
            raise SoapException(f'Action should start with "/": {action}')

        action = action[1:]
        
        payload_nd = _get_xml_node(root, 'Body/' + lcamel(action) + 'Request')
    else:
        if is_fault_action(action):
            payload_nd = _get_xml_node(root, 'Body/Fault')
        else:
            if not action.startswith('/'):
                raise SoapException(f'Action should start with "/": {action}')

            action = action[1:]

            #if not action.endswith('Response'):
            #    raise SoapException(f'Response Action should end with "Response": {action}')
        
            body_nd = _get_xml_node(root, 'Body')
            payload_nd = body_nd[0]
    
    res = SoapMessage(action, _parse_payload(payload_nd))
    res.MessageID = unqualify_id(_t(root, 'Header/MessageID'))
    
    if is_request:
        res.ChargeBoxIdentity = _t(root, 'Header/chargeBoxIdentity')
    else:
        res.RelatesTo = unqualify_id(_t(root, 'Header/RelatesTo'))
    
    return res

