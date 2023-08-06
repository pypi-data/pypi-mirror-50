import paho.mqtt.client as mqtt
import json


class Service(object):
    # defult
    def __init__(self,username,password):
        self.username = username
        self.Client = mqtt.Client()
        self.Client.username_pw_set(username,password)
        self.Client.connect("167.71.219.4",1883)

    # Send msg
    def SendMQ(self,msg):
        self.Client.publish(topic="/"+self.username, payload=msg)

    # Send json
    def SendDB(self,table,tag,value):
        msg = { 
            "database": self.username,
            "data":[{
                "measurement":table,
                "tags":{
                    "tag" : tag,
            },
            "fields": {
                    "value": value
                }
            }]
        }
        msg =json.dumps(msg)
        self.Client.publish(topic="/"+self.username, payload=msg)

    # Send Map
    def SendMap(self,table,lat,longt,tag,value):
        msg = { 
                    "database": self.username,
                    "data":[{
                        "measurement":str(table),
                        "tags":{
                            "tag" : tag,
                            "latitude": str(lat),
                            "longitude": str(longt),
                    },
                    "fields": {
                            "value": value
                        }
                    }]
                }
        msg =json.dumps(msg)
        self.Client.publish(topic="/"+self.username, payload=msg)

