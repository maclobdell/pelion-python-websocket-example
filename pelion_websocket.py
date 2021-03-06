#!/usr/bin/python3
import sys, pycurl, certifi, websocket, json, base64
from io import BytesIO

def main(argv):

    #get api key from command line argument
    if len(sys.argv) > 1:
        api_key = argv[0]
    else:
        print("Error: please pass API KEY")
        sys.exit()

    create_websocket(api_key)

    device_id = '0172b9ba5409000000000001001117f5'  #change this to your device
    resource_uri = '/3200/0/5501'  #digital counter resource used in mbed-os-example-pelion

    subscribe_to_resource(api_key,device_id,resource_uri)


def create_websocket(api_key):

#enable websocket notification channel

    #prepare request and buffer for response
    buffer = BytesIO()
    header = []
    header.append("Authorization: Bearer " + api_key)
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.us-east-1.mbedcloud.com/v2/notification/websocket')
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.NOPROGRESS,1)
    c.setopt(c.NOBODY,1)
    c.setopt(c.HEADER,1)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.TCP_KEEPALIVE,1)

    #execute request
    c.perform()
    c.close()

    #print response
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))

#connect to registered websocket and open the channel
    websocket.enableTrace(True)
    header = []
    header.append("Authorization: Bearer " + api_key)

    ws = websocket.WebSocketApp("wss://api.us-east-1.mbedcloud.com/v2/notification/websocket-connect",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              header = header
                              )

    ws.on_open = on_open
    ws.run_forever()


def on_message(ws, message):
    print(message)
    #example notification that this parses
    #{"notifications":[{"ep":"0172b9ba5409000000000001001117f5","path":"/3200/0/5501","ct":"text/plain","payload":"NzE=","max-age":0}]}

    #convert from string to dict object
    msg = json.loads(message)
    #parse message for notifications
    for notification in msg['notifications']:
        #check for the device id, not always the same as endpoint id, but called endpoint here
        if "ep" in notification:
            ep = notification['ep']
            print("device: " + ep)
        #check for the resource uri, aka path
        if "path" in notification:
            resource_uri = notification['path']
            print("resource: " + resource_uri)
        #check for the resource value, aka payload
        if "payload" in notification:
            resource_value = str(base64.b64decode(notification['payload']))
            print("value: " + resource_value)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")


def subscribe_to_resource(api_key,device_id,resource_uri):

    #prepare request and buffer for response
    buffer = BytesIO()
    header = []
    header.append("Authorization: Bearer " + api_key)

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.us-east-1.mbedcloud.com/v2/subscriptions/' + device_id + resource_uri)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.NOPROGRESS,1)
    c.setopt(c.NOBODY,1)
    c.setopt(c.HEADER,1)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.CUSTOMREQUEST, "PUT")
    c.setopt(c.TCP_KEEPALIVE,1)

    #execute request
    c.perform()
    c.close()

    #print response
    body = buffer.getvalue()
    print(body.decode('iso-8859-1'))


if __name__ == "__main__":
    main(sys.argv[1:])
