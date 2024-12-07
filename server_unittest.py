import json
import unittest
from server import Server



class TestServerMethod(unittest.TestCase):
    def setUp(self):
        self.server = Server()



    def test_execute_os_command(self):
        request_1 = {'command_name': 'echo', 'parameters': ['HelloWorld']}
        request_2 = {'command_name': 'echo', 'parameters': 'HelloWorld'}
        request_3 = {'command_name': 'echo HelloWorld', 'parameters': {}}
        request_4 = {'command_name': 'echo HelloWorld', 'parameters': None}
        request_5 = {'command_name': 'wrongcommand', 'parameters': ''}


        response = self.server.execute_os_command(request_1.get('command_name'), request_1.get('parameters'))
        self.assertEqual(response['status'], 'success')
        self.assertIn('HelloWorld', response['result'])

        response = self.server.execute_os_command(request_2.get('command_name'), request_2.get('parameters'))
        self.assertEqual(response['status'], 'success')

        response = self.server.execute_os_command(request_3.get('command_name'), request_3.get('parameters'))
        self.assertEqual(response['status'], 'success')

        response = self.server.execute_os_command(request_4.get('command_name'), request_4.get('parameters'))
        self.assertEqual(response['status'], 'success')

        response = self.server.execute_os_command(request_5.get('command_name'), request_5.get('parameters'))
        self.assertEqual(response['status'], 'error')



    def test_process_request(self):
        request_1 = json.dumps({'command_type': 'os', 'command_name': 'echo', 'parameters': 'HelloWorld'})
        request_2 = json.dumps({'command_type': 'compute', 'expression': '(40 + 60) * 2'})
        request_3 = json.dumps({'command_type': 'invalid', 'command_name': 'echo', 'parameters': 'HelloWorld'})
        request_4 = {'command_type': 'os', 'command_name': 'echo', 'parameters': 'HelloWorld'}


        response = self.server.process_request(request_1)
        self.assertEqual(response['status'], 'success')

        response = self.server.process_request(request_2)
        self.assertEqual(response['status'], 'success')

        response = self.server.process_request(request_3)
        self.assertEqual(response['status'], 'error')
        
        response = self.server.process_request(request_4)
        self.assertEqual(response['status'], 'error')



    def test_execute_math_command(self):
        request_1 = {"expression": "__import__('subprocess').getoutput('echo hellow')"} # injecting os command with subprocess lib
        request_2 = {'command_type': 'compute', 'expression': '1 / 0'}                  # division by zero
        request_3 = {'expression': '(40 + 60) * 2'}


        response = self.server.execute_math_command(request_1.get("expression"))
        self.assertEqual(response["status"], "error")
        self.assertIn("'NoneType' object is not subscriptable", response["result"])

        response = self.server.execute_math_command(request_2)
        self.assertEqual(response["status"], "error")

        response = self.server.execute_math_command(request_3.get('expression'))
        self.assertEqual(response['status'], 'success')
        self.assertEqual(response['result'], 200)



if __name__ == "__main__":
    unittest.main()