import unittest
import threading
import paramiko
import redssh

from . import paramiko_server



class RedSSHUnitTest(unittest.TestCase):

    def setUp(self):
        self.paramiko_server = threading.Thread(target=paramiko_server.start_server)
        self.paramiko_server.start()

    def tearDown(self):

    def wait_for(self, wait_string):
        if isinstance(wait_string,type('')):
            wait_string = wait_string.encode('utf8')
        read_data = b''
        while not wait_string in read_data:
            for data in self.rs.read():
                read_data += data
        return(read_data)

    def sendline(self, line):
        self.rs.send(line+'\r\n')

    def test_basic(self):
        rs = redssh.RedSSH()
        rs.connect('localhost', 2200, 'robey', 'foo')
        self.wait_for(b'Command: ')
        self.sendline('reply')
        self.wait_for('END OF TEST')
        rs.exit()


if __name__ == '__main__':
    unittest.main()

