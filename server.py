import zmq
import json
import logging
import platform
import subprocess
import concurrent.futures



def beautiful_str(value):
    """
    Description: This function beautifies the any type entries for logging.
    value = dict | list | tuple | set | str | int | float \n
    """

    FinalMSG, slicer = '', '_________________________________________________________'
    if isinstance(value, dict):
        for key1, value1 in value.items():
            if isinstance(value1, dict):
                nested = ''
                for key2, value2 in value1.items():
                    nested += f'\n\t\t{key2} : {value2}'
                FinalMSG += f'\t{key1} : {nested}\n'
            elif not isinstance(value1, dict):FinalMSG += f'\t{key1} : {value1}\n'
        FinalMSG = f'{FinalMSG}\n{slicer}'

    elif not isinstance(value, dict): FinalMSG = f'\t{value}\n{slicer}'
    return FinalMSG



class Server:
    """
    Description:\n
        This program is run on server side & allows client to \n
        execute commands & perform mathematical calculations \n
        on the server side. \n
    backend_address: \n
        The address for your server(worker)\n
    frontend_address: \n
        This address for the frontend (the frontend(zmq device) is between clients & servers. \n
        The address is for communication with the clients \n
        clients -> frontend(zmq device) <- servers(backend) \n
    """
    def __init__(self, backend_address:str='tcp://localhost:5060', frontend_address:str='tcp://localhost:8000', capture_log:bool=True, verbos:bool=True):
        self.backend_address = backend_address
        self.frontend_address = frontend_address
        self.verbos = verbos

        # if operating system is Windows, it execute the command in PowerShell
        self.active_power_shell = 'powershell' if platform.system() == 'Windows' else None

        # set basic config for logging
        self.capture_log = capture_log
        if capture_log:
            logging.basicConfig(filename='server.log', filemode='w', encoding='utf-8', level=logging.DEBUG, datefmt='%H:%M:%S',format='%(levelname)s\tTime : %(asctime)s\t\t%(message)s')


    def _log(self, request:json, response:dict) -> None:
        """save client activity into client.log"""
        request = json.loads(request)
        my_log = {}
        my_log.update(request)
        my_log.update(response)
        log_level = 'info' if my_log.get('status', '') == 'success' else 'error'
        b_log = beautiful_str(my_log)
        
        if   log_level == 'info' : logging.info(b_log)
        elif log_level == 'error': logging.error(b_log)



    def execute_os_command(self, command:str, parameters:list=[]) -> dict:
        """Description: execute os command by parameter in operating system"""
        # check if parameter isinstance str : add parameter to list -> [parameter]
        parameters = [parameters] if isinstance(parameters, str) else parameters
        # check if parameter == None -> set parameter to empty list []
        parameters = [] if isinstance(parameters, (dict, type(None))) else parameters

        try:
            result = subprocess.run([self.active_power_shell, command, *parameters], capture_output=True, text=True, shell=True)
  
            if result.stderr:
                return {'status': 'error', 'result': result.stdout, 'error': result.stderr}
            return {'status': 'success', 'result': result.stdout, 'error': result.stderr}
        
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        

    def execute_math_command(self, expression:str) -> dict:
        """Description: Calculate string expression with eval function"""
        try:
            result = eval(expression, {'__builtins__': None}, {'__builtins__': None})
            return {'status': 'success', 'result': result}
        except Exception as e:
            return {'status': 'error', 'result': str(e)}
        

    def process_request(self, request:json) -> dict:
        """Description: Handle os & compute command and send the request to the relevant method"""
        try:
            command = json.loads(request)
            command_type = command.get('command_type', '').lower()

            if command_type == 'os':
                return self.execute_os_command(command.get('command_name', ''), command.get('parameters', []))
            
            elif command_type == 'compute':
                return self.execute_math_command(command.get('expression', ''))
            
            else:
                return {'status': 'error', 'result': 'Invalid command type'}
            
        except Exception as e:
            return {'status': 'error', 'error': e}


    def _queue_device(self):
        """
        Description: 
            This is the intermediary that sits between clients & servers.
            forwarding request to servers & relaying replies back to client.
        """
        context = zmq.Context(1)
        frontend = context.socket(zmq.XREP)
        frontend.bind(self.frontend_address)
        backend = context.socket(zmq.XREQ)
        backend.bind(self.backend_address)
        zmq.device(zmq.QUEUE, frontend, backend)


    def _queue_server(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect(self.backend_address)
        while True:
            request = socket.recv_string()
            response = self.process_request(request)
            socket.send_string(json.dumps(response))
            if self.capture_log: self._log(request, response)
            if self.verbos:
                print(f'\n{request}\n{response}')


    def run(self, worker:int=10):
        """
        Description: \n

            first:  runing the device \n
            second: adding the server for range number of worker in the pool for concurenty 
        """
        if self.verbos: print('starting server')
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=15)
        pool.submit(self._queue_device)
        if self.verbos: print('binding device')
        for i in range(worker):
            if self.verbos: print(f'worker {i} started')
            pool.submit(self._queue_server)
        if self.verbos: print('server is up ...')
        pool.shutdown(wait=True)



if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('-B', '--backend_address', type=str, default='tcp://localhost:5060', help="The address for your server(worker), default: 'tcp://localhost:5060'")
    parser.add_argument('-F', '--frontend_address', type=str, default='tcp://localhost:8000',
                         help="This address for the frontend (the frontend(zmq device) is between clients & servers.\
                         The address is for communication with the clients. clients -> frontend(zmq device) <- servers(backend), default: frontend_address:str='tcp://localhost:8000'")
    parser.add_argument('-W', '--worker', type=int, default=10, help='adding the server for range number of worker in the pool for concurenty')
    parser.add_argument('-L', '--log', type=int, default=True, help='if True: capture log is activate in server.log')


    args = parser.parse_args()
    try:
        backend_address, frontend_address, worker, log = (args.backend_address, args.frontend_address, args.worker, args.log)
        server = Server()
        server.run(worker)

    except Exception as e:
            print(e)