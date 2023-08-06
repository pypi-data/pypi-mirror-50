import uuid
import xml.etree.ElementTree as ET

from .soap import SoapMessage, lcamel, ucamel, fqid


def _create_text_elt(parent, name, text):
    elt = ET.SubElement(parent, name)
    elt.text = text
    return elt


def _build_payload(xml_nd, payload: dict):
    for k, v in payload.items():
        sub_elt = ET.SubElement(xml_nd, k)
        if isinstance(v, dict):
            _build_payload(sub_elt, v)
        else:
            sub_elt.text = str(v)


def build_msg(msg: SoapMessage, is_request: bool, is_cs: bool = False) -> bytes:
    """
        MessageID можно не заполнять - будет установлен автоматически
    """
    assert isinstance(msg, SoapMessage), msg
    assert msg.Action and isinstance(msg.Action, str), msg
    
    tree = ET.ElementTree()

    Envelope = ET.Element('soap:Envelope', attrib={
        'xmlns:soap':       'http://www.w3.org/2003/05/soap-envelope',
        #'xmlns:cp':         'urn://Ocpp/Cp/2012/06/',
        'xmlns:wsa5':       'http://www.w3.org/2005/08/addressing',
        'xmlns:cs':         'urn://Ocpp/Cs/2012/06/'
    })
    
    Header = ET.SubElement(Envelope, 'soap:Header')
    
    # chargeBoxIdentity
    if is_request:
        _create_text_elt(Header, 'cs:chargeBoxIdentity', msg.ChargeBoxIdentity)
    
    # Action
    Header_Action = ET.SubElement(Header, 'wsa5:Action', attrib={'soap:mustUnderstand': 'true'} if is_request else {})
    Header_Action.text = '/' + msg.Action
    
    # MessageID
    if not msg.MessageID:
        msg.MessageID = str(uuid.uuid4())
    _create_text_elt(Header, 'wsa5:MessageID', fqid(msg.MessageID))
    
    # To    
    Header_To = ET.SubElement(Header, 'wsa5:To', attrib={'soap:mustUnderstand': 'true'} if is_request else {})
    Header_To.text = msg.CentralStationAddress if is_request else 'http://www.w3.org/2005/08/addressing/anonymous'
    
    # From
    if is_request:
        if msg.ChargerPublicAddress:
            Header_From = ET.SubElement(Header, 'wsa5:From')
            _create_text_elt(Header_From, 'wsa5:Address', msg.ChargerPublicAddress)
        else:
            pass
    
    # ReplyTo
    if is_request:
        Header_ReplyTo = ET.SubElement(Header, 'wsa5:ReplyTo')
        _create_text_elt(Header_ReplyTo, 'wsa5:Address', 'http://www.w3.org/2005/08/addressing/anonymous')
    
    # RelatesTo
    if not is_request:
        Header_RelatesTo = ET.SubElement(Header, 'wsa5:RelatesTo')
        Header_RelatesTo.text = fqid(msg.RelatesTo)
    
    Body = ET.SubElement(Envelope, 'soap:Body')
    
    if msg.is_fault():
        payload_nd = ET.SubElement(Body, 'Fault', attrib={'xmlns': 'http://www.w3.org/2003/05/soap-envelope'})
    else:
        payload_nd_name = lcamel(msg.Action) 
        if is_request:
            payload_nd_name += 'Request'
        payload_ns = 'urn://Ocpp/Cs/2012/06/' if is_request else 'urn://Ocpp/Cp/2012/06/'
        payload_nd = ET.SubElement(Body, payload_nd_name, attrib={'xmlns': payload_ns})
        
    _build_payload(payload_nd, msg.Payload)
    
    return b'<?xml version="1.0" encoding="UTF-8"?>' + ET.tostring(Envelope)
