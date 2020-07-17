# Pelion Device Management Python Websocket Example

This is a simple example using python packages pycurl and websocket-client to set up a websocket notification channel with Pelion Device Management

This allows you to subscribe to resources and get notifications if they change.

Created by Mac Lobdell

## Setup

Install Python 3 (I tested this with Python 3.7.6), then run the following commands.

```
pip install pycurl
pip install websocket-client
```

## Usage

Connect a device to Pelion Device Management and get an API key. Follow the guide at https://www.pelion.com/guides/connect-device-to-pelion/.

Open `pelion_websocket.py`, change the `device_id` to a device you have connected. You can get that information on the device's serial terminal when it registers to Pelion or in the Pelion Device Management Console. Note that you can get notifications on large groups of devices, but for this example, it just uses one.

Then run the script:

`python pelion_websocket.py <API_KEY>`

In the device's serial port, send characters to the device by typing on a keyboard. This will increase the simple counter resource on the device.

On the Device's serial port

`Counter 57`

On the notification channel, you should get a message such as:

`#{"notifications":[{"ep":"0172b9ba5409000000000001001117f5","path":"/3200/0/5501","ct":"text/plain","payload":"NzE=","max-age":0}]}`

There can be multiple notifications in a message.

The notifications are parsed and the device id, resource uri, and payload are decoded and printed.

```
device: 0172b9ba5409000000000001001117f5
resource: /3200/0/5501
value: b'57'
```

The payload value is encoded in Base64. For example, decoding the value `NTc=` results in `57`.

To close the websocket, press CTRL+C to kill the process.
