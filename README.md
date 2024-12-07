## repo introduction -> __server client application__ with ZMQ
### Hello :)
#### This lib contains two programs.
#### One is on the __client__ side and the other is on the __server__ side.
#### Well, let's do a short review on this lib.
## The __server__ side :
#### server.py in the first step runs a device.
### more info for the device :
#### The device is the interface between the client and the socket nodes.
#### It listens the __frontend__ and is connected to the __backend__ (socket nodes)
#### device can listen to a specific address and After load balancing, it sends the request to one of the nodes.

![device](https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/_images/zmqdevices.png)

### I implemented this method ->

![device](https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/_images/Queue.png)

#### For more information you can read this __[Article](https:/learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html)__
#### After receiving the __Json__ request:
#### __Checks the request__
#### __Executes the commands__
#### __Returns the answer as Jason__
#### The server understand two types of commands: expression & system commands.

    exp:
        '{"command_type": "os", "command_name": "echo", "parameters": "HelloWorld"}'
        '{"command_type": "compute", "expression": "(40 + 60) * 2"}'

## The __client__ side :
#### This program sends your requests to the server through a socket connection.
### __usage__ :
#### __mode  os__ : you can send system commands to the server.
#### __mode  compute__ : you can perform your mathematical calculations on the server side.

#### Finally, you can recive the __Json__ response.

### You can run the client side program in two ways.

#### 1 __->__ you can create an instance of the Client class and send the input in the form of send_request method.

    from client import Client

    import json

    dict_request = {'command_type': 'os', 'command_name': 'echo', 'parameters': 'HelloWorld'}

    json_request = json.dumps(dict_request)

    client = Client()

    print(client.send_request(json_request))

#### 2  __->__ You can also send arguments in the __$hell->__

        exp 1: python .\client.py --mode='os' --command='ping 127.0.0.1' --arg='-n 6'

        exp 2: python .\client.py --mode='compute' --expression='5*5'

#### Enter this command in the terminal to see how to do this __$hell->__

    python client.py --help

#### For __Test__ the server, you can enter the command in the  __$hell->__
    python server_unittest.py


#### Installion of libraries :
    pip install -r requirements.txt