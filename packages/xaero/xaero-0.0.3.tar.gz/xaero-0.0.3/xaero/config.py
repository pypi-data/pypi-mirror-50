
CONFIG = {
    "clouds":{
        "default": "production",
        
        "local":{
            "soap": "http://localhost:8080/steve/services/CentralSystemService",
            "ws": "ws://localhost:8080/steve/websocket/CentralSystemService"
        },
        "steve":{
            "soap": "http://steve.v4d.online:8080/steve/services/CentralSystemService",
            "ws": "ws://steve.v4d.online:8080/steve/websocket/CentralSystemService"
        },
        "staging":{
            "-soap": "http://staging.v4d.online:8080/steve/services/CentralSystemService",
            "ws": "ws://staging.v4d.online:5101/ocpp15",
            "constraints":["cn.zaria.timestamp"]
        },
        "test.v4d.ru":{
            "--soap (tomcat is off)": "http://test.v4d.ru/soap",
            "ws": "ws://test.v4d.ru/isws/ocpp15",
            "constraints":["cn.zaria.timestamp"]
        },
        "setec":{
            "soap": "http://is.v4d.online:8889/soap",
            "constraints":["cn.zaria.timestamp"]
        }
    },
    
    "hardware":{
        "evlink":{
            "nbConnectors": 1,
            "meta":{
                "chargePointVendor": "Schneider Electric",
                "chargePointModel": "EVlink Smart Wallbox",
                "firmwareVersion": "3.2.0.12",
                "chargePointSerialNumber": "3N170740564A1S1B7551700014",
                "chargeBoxSerialNumber": "EVB1A22P4RI3N1712406002002503A057"
            }
        },
        "setec":{
            "nbConnectors": 3,
            "meta":{
                "chargePointVendor": "5454",
                "chargePointModel": "35",
                "chargePointSerialNumber": "65",
                "chargeBoxSerialNumber": "75",
                "firmwareVersion": "65",
                "iccid": "78",
                "imsi": "78",
                "meterType": "7",
                "meterSerialNumber": "8"
            }
        }
    },
    
    "chargers":{
        "default":{
            "id": "FOO",
            "model": "evlink",
            "meta":{
            }
        },
        "foo":{
            "id": "423242",
            "model": "evlink",
            "meta":{
                "chargeBoxSerialNumber": "ololo"
            }
        },
        "setec":{
            "id": "423242",
            "model": "setec",
            "meta":{
            }
        }
    },
    
    "tags":{
    }
}
