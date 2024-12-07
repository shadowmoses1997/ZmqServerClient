import zmq
import json




class Client:
    def __init__(self, host:str='localhost', port:int=8000):
        self.address = f'tcp://{host}:{port}'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.address)
        print(f"Client connected to server at {self.address}")

    def send_request(self, command):
        try:
            self.socket.send_string(command)
            response = self.socket.recv_string()
            load_response = json.loads(response)
            return json.dumps(load_response, indent=1)
        except Exception as e:
            return {"status": "error", "message": str(e)}
        


if __name__ == '__main__':
    import argparse
    import ipaddress


    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', default='localhost', help="set your destination ip address, default: '127.0.0.1'")
    parser.add_argument('-P', '--port', type=int, default=8000, help="set your destination port, default: 8000")

    parser.add_argument('-M', '--mode', type=str, help='select client app mode, modes -> "os", "compute"')

    # mode os
    parser.add_argument('-C', '--command', type=str, help='write your command -> "ping 127.0.0.1"')
    parser.add_argument('-A', '--arg', type=str, help='write your argument -> "-n 6"')

    # mode compute
    parser.add_argument('-E', '--expression', type=str, help='write your expression -> "5*5"')

    args = parser.parse_args()

    if args.mode == 'os':
        command = {'command_type':args.mode, 'command_name':args.command, 'parameters':args.arg}

    elif args.mode == 'compute':
        command = {'command_type':args.mode, 'expression':args.expression}

    else:

        exit()
        
        #     Hello :)
        #       This lib contains two programs.
        #       One is on the [client] side and the other is on the [server] side.
        #       Well, let's do a short review on this lib.
        #       The server side:
        #       server.py in the first step runs a device.
        #       more info for the device :
        #       The device is the interface between the client and the socket nodes.
        #       It listens the frontend and is connected to the backend(socket nodes)
        #       device can listen to a specific address and After load balancing, it sends the request to one of the nodes.
        #       frontend(client) <-> zmq_device <-> server(socket nodes)
        #       for more information you can read this article -> https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/queue.html
        #       After receiving the Json request:
        #       Checks the request.
        #       Executes the commands.
        #       Returns the answer as Jason.
        #       The server understand two types of commands: expression & system commands.
        #       exp:
        #       '{"command_type": "os", "command_name": "echo", "parameters": "HelloWorld"}'
        #       '{"command_type": "compute", "expression": "(40 + 60) * 2"}'

        #       The client side:
        #       This program sends your requests to the server through a socket connection.
        #       usage:
        #       mode  os: you can send system commands to the server.
        #       mode  compute: you can perform your mathematical calculations on the server side.
        #       Finally, you can recive the Json response.
              
        #       You can run the client side program in two ways.
        #       1 -> you can create an instance of the Client class and send the input in the form of send_request method.
        #       2 -> you can give the arguments to the program input.
        #       exp 1: python .\client.py --mode='os' --command='ping 127.0.0.1' --arg='-n 6'
        #       exp 2: python .\client.py --mode='compute' --expression='5*5'
        #       Enter this code in the terminal to see how to do this $-> python client.py --help""")
        


    try:
        ip   = args.ip if args.ip == 'localhost' else str(ipaddress.ip_address(args.ip))
        port = int(args.port)

        client = Client()
        res = client.send_request(json.dumps(command))
        res = json.loads(res)
        if res.get('status') == 'success': print(res.get('result'))
        elif res.get('status') == 'error': print(res.get('error'))

    except Exception as e:
            print(e)