import socket
import threading
from StringIO import StringIO
from abc import abstractmethod
from time import sleep
from unittest import TestCase, skip

import paramiko
from paramiko import PasswordRequiredException
from paramiko import RSAKey
from paramiko import SSHException

from cloudshell.cli.session.ssh_session import SSHSession, SSHSessionException
from mock import Mock, patch


KEY_WITHOUT_PASSPHRASE = '''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAy3c5WDz+EY0itrUjRXsDL3DK0nVrvfkvArdORajNT/mjThfh
aUT8sCin0Abg8IiOcBFA35GutAUJGiJ0TEeIJzSHJmZoyRqeXSyP+cnPJ2I6n96J
Q6+dfeP+yKNhtNrqSZ0Tb7BLjogeVyHNaTiQESRs7tl1q8kzqG5Bz6JfkqxFt1J0
3WCiPu4e5ZwLJTXoiXfJhc8Ja0WztkT0e/bXgVEdrvB6enxP5uWWOo0U/61SyvWe
3nVvBwtdZiNY2ltDEM+uhPOSby8+cUOH7T+U3YLuIuMBgGTHHZxwcCzC6EYUFYjd
7B21x4s0lU7OVEI0OYV2BJfscBtB3+e00ytyGwIDAQABAoIBAB/RqFUlTLJf+QLL
txVhlHDx2bYqCMxv0KtDEWmRaXJNXv2SfHzi/gVqhjvhJ4JWSLg76oJMHR8n/nFo
2/kl4qQG8e/OaiqxD/0QP//XUJ8fHH3t5leAeke6xRiJfHk1FximCOkZj+ddYClO
Lvp6jwUvRh3gQie4UmzPuVkIUpv0L1/RrGoL+JDBWsoHULxUxAUEgFcClnnQMkbZ
tGRAUfo1I9bLzoIXDGCkIiIDuF4NHwj80HJmbf2bCbrsP9BFfOqOe7vm5fzBP+B9
ps0+NRp3Np7ZwGY4b7YqChTfISouSWuLl8F8faICE3Fgtl0dtqhdb/Dd+Z5c8U2+
DLWZD/ECgYEA96RbBvA+S7IRTFUUTZ+Zd7DQTuU5kVtQIakCkNH1611xT5vVJsSK
Z+DZVehd5Tm1+1lWk1LZCvnahzrlekYt+dmB6Y2XlM9AyxgW5GRifHWlp7xc4xDQ
hiAX4Mv+clAcz/S/gSFcttk78gMapZhova4vM5bYPtvOG4IZ3Gt6kPkCgYEA0lUu
oAOnmwwAujOPMI39vxuh4AAaClLiNdToyXnHN6karVR7r0hm/eMdpEEnKLw2aLNx
MxSLK9M3TCqK9VIgnhC6SrBn6HO24jUXxltNsA48NuM0fAEa9lDgMwzIoNdRw/hL
/XlLWKO7gO4RsiRuPOsAIKaZ0vzrnnGaVE4RtLMCgYBDgXkS3iCNL+BJR5P+SPhj
yT4vk4rq1dJ1KoY5hhKcc191DQzAwajdAk0cfvhBiUbTWpogFOB3fn6UiHiPqVvV
FPa1/NQKS6jk9A8heT/jn4plvBIyD55YQZ1guRsGfFIuWhBuGfMVIQiXQ0NbSr2a
n0XcsU0HbZG0q/VywZWquQKBgENOlvkFsmDfWmw7i5rSFV1OjmKMJckf9NudIlE2
8xVQvASzgFD7LloYj6e8YbebYx3mLldWP6LqmEt7YbRXb7ClUbgM83NjdCa3LsB+
/0FTjNlTo7v67pHcF6K+eIVf4f6AOnEGm6Hl417C0E7dcZl06jmIlrj5zryJRgWs
ZeYZAoGAeNci+ovfvY9k1vLu/vObSBxeFy0XRW2Sb7WVgX5bVOiB59+SPtrl1+5K
YQQOac/uJaoBYGWlBS+2TufB6QS0LREi5k/CkvmN+cTg8U5QkyRZpltjJnIxDXLC
IhTaHWMNXatAhwWfKUJR++xBK5Gb2gpwQax4P5Cz6fukg4prEKg=
-----END RSA PRIVATE KEY-----
'''

KEY_WITH_PASSPHRASE = '''-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,E81B330B3A278826D82BEBBC87DE2689

o5HgSflyaNgr58eQbpzT+Mns1jGe1ni6+BfvOH2L802TISoihKKLzw4RQySJC7AG
voE+HieCdyAmrQ63xob3vu09GkJO/JOh1qBRPh7uhqX0T0VQM1cMy6j1yQsylpPC
iQ0+2MqBQlrldJBQ5SdwoV9I3ffo5AzJ76IpnfzIQezcNS0q23MKOVxJR6j7Zffe
rj4pODyfKVfBIbpFcvQKZhUcoZIqIhm+8Gsu45hRn/hjz0cyV3YmMv50S7onOqSi
aaYnCWQ79TndNAFW0GE38C3SdZa6S0UXHKVyx52T3uriUGDv/2Vxkbm4Z8bwcTPx
vYebH4Yme2MX/HZkRD49at0lDtglyPqQNjlDhdV6RYEDKYH8AXWlaR2oafTCY8D3
bmNhRKP5mfqoPBta6DCSbEvKcYTRkiv4TLrn4W15671izWooZSzQHn3yYJQv/wPX
g7uzEjM3l0V5qB6eMKeoFZ6ZdPtnynpRBBpmbzVEf6ae6xLopV5kxBs1w6NSDNfY
s71Dol2VkiDWNCHcVO4bHMgxeKRtMaLFZ/XAUlyRklxwTwRGC0wY2XeHneo/Qr5S
RmhYFttIAK+/STsoO3Z6DYGnFw+djhz/3Lbrhv8bfyIpubMqS7CfwAXQgrNWjPyX
weCvgs829JZlnkyd5mUTobRKnnLVmumy3A2THb2iYeNToxmjIeXRaA9qaZKMUGH1
R56AdbS3heX90N0ZFywMm5/TIUOciUER/P6hwAs6Lywmb3IYMNN8SCnfWxN047B7
OJQGxCpg0/VxfZV5iOAqqWyqO684cbSF8RjA8LxnrMlWvpkj2+NXQm9GDyLB3FqC
1KFE0e5a872upFOiQ13dkFRLSzxE/Y6FaphmkC6AKMq5CARUC94j/uItIpCeSmzX
VQIvRJwsBqy4CJtuD1kJwQQu6cZ7cnJ60OL0et2idPaeNnNl1f5fsZyzGFaJ8IcF
u+d7P/T+bNpC70EasD2hn/KUX61//3ScGuIkSJeX/u0DGjddkfdgzgRluB1YqpHT
3ERx3evUoZypYcF+e8BtkrR4ARaNfRj27OPQPf6q1CFFPPvK21dpsgJsDRztsp2n
+A1LLJMYpOhcc/pRc8zWpSuXtJ7y9lMUvWWTVm+saaVA6tZEo0ZqAbUK02Ob0Wdd
bLIBXUPX8wvgYsGgNuy1jQNMSeygOWQ/VitSCMuMTWMg4tuQ2cIMNE8Y0ngwyamb
/wAOebZYlD9MegGd3N8Ijc2SSGfz4nkOaTLEjhHDLcYO3TGL35wbJYlsa3QcjVPK
VrTjSUBlRyEZu1r61Izo4ah1gwJpNjmQu3oe6+MU/GqI3BC3v7HQtj+MGklBwc0I
r73roiEftLm95vMH8P+ksmis0ha8aFyXpOXdWfxLUz7RUp5PhdPkIgVyV1OvyVPh
y9/ziFJPPMN703N1dJ0e1oRWpfSFUzlGn1OgF1EY9qQTwQK4PL9bhyJi1/MswZHB
/XmDlKr7An89Iy+B/Q9ncja2FfK49AP23AMYKhdWBrEq+enXwjkr5Uz8ffD3eagD
VZxBlCGUp4bmlS5s7sttMZRvJq0CXfxy+q8Qe0sz/CyOAN/J8iZu8AJyp04DQk4d
-----END RSA PRIVATE KEY-----
'''
KEY_PASSPHRASE = 'quali1234'


class FakeDevice:
    def __init__(self):
        pass

    @abstractmethod
    def get_banner(self):
        """

        :return: str : the welcome banner of the fake device
        """
        pass

    @abstractmethod
    def do_command(self, command):
        """

        :param command: command to execute
        :return: (str, str, int) stdout, stderr, return code
        """
        pass


class DefaultFakeDevice(FakeDevice):
    NORMAL_PROMPT = '[prompt] $ # > '
    ENABLE_PROMPT = '[enable] $ # > '

    def __init__(self):
        FakeDevice.__init__(self)
        self.prompt = self.NORMAL_PROMPT

    def get_banner(self):
        """

        :return: str
        """
        return '--------------\nWelcome to the default fake device\n--------------\n%s' % self.prompt

    def do_command(self, command):
        """

        :param command: str : command to execute
        :return: (str, str, int) : stdout, stderr, return code
        """
        if command == 'enable':
            self.prompt = self.ENABLE_PROMPT
        if command == 'exit':
            self.prompt = self.NORMAL_PROMPT
        output = ''.join(['%s ' % s for s in command])  # c o m m a n d
        return '%s\noutput of "%s"\n%s' % (command, output, self.prompt), '', 0


class SSHServer(paramiko.ServerInterface):
    def __init__(self,
                 listen_addr='127.0.0.1',
                 port=0,
                 server_key_string=None,
                 user2key=None,
                 user2password=None,
                 fake_device=None,
                 enable_sftp=False,
                 enable_scp=False,
                 *largs, **kwargs):
        """

        :param listen_addr: str : which local IP to listen on, default 127.0.0.1
        :param port: int : listening port for the SSH server, or 0 to let the system choose; if 0 was used, check the .port field for the assigned port
        :param server_key_string: str : private key for the server's identity; leave blank to generate
        :param user2key: dict[str, PKey] : mapping from each username to the correct public or private PKey
        :param user2password: dict[str, str] : mapping from each username to the correct password
        :param fake_device: FakeDevice : an object that responds to commands
        :param enable_sftp: bool : whether to respond to SFTP requests
        :param enable_scp: bool : whether to respond to SCP requests
        :param largs:
        :param kwargs:
        """

        paramiko.ServerInterface.__init__(self)
        self.enable_sftp = enable_sftp
        self.enable_scp = enable_scp
        self.user2key = user2key or {}
        self.user2password = user2password or {}
        self.fake_device = fake_device or DefaultFakeDevice()
        self.server_key = RSAKey.from_private_key(StringIO(server_key_string)) if server_key_string else RSAKey.generate(2048)
        self.reads = {}
        self.sftpfilename2stringio = {}
        self.channelid2scpfilename = {}
        self.channelid2subsystem = {}
        self.channels = set()
        self.scpchannelid2command = {}
        self.channelid2event = {}

        self.listensock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listensock.bind((listen_addr, port))
        self.listensock.listen(5)
        self.port = self.listensock.getsockname()[1]

        t = threading.Thread(target=self.sockthread)
        t.setDaemon(True)
        t.start()

    def sockthread(self):
        while True:
            try:
                conn, addr = self.listensock.accept()
                if not conn:
                    return
            except:
                return

            self.transport = paramiko.Transport(conn)
            self.transport.add_server_key(self.server_key)
            if self.enable_sftp:
                self.transport.set_subsystem_handler('sftp', SFTPHandler)

            self.transport.start_server(server=self)

            t2 = threading.Thread(target=self.transportthread)
            t2.setDaemon(True)
            t2.start()

    def transportthread(self):
        # print 'starting transport thread'
        while True:
            ch = self.transport.accept()
            if ch is None:
                # print 'transport accept None channel'
                return
            # print 'transport accept channel %d' % ch.get_id()

            self.channels.add(ch)

    def session_thread(self, channel):
        # print 'starting session thread %d' % channel.get_id()
        self.reads[channel.get_id()] = []
        channel.sendall(self.fake_device.get_banner())
        buf = ''
        while True:
            b = channel.recv(1024)
            self.reads[channel.get_id()].append(b)
            if len(b) > 0:
                buf += b
            if buf.endswith('\n') or buf.endswith('\r'):
                buf = buf.strip()
                o, e, _ = self.fake_device.do_command(buf)
                if o:
                    channel.sendall(o)
                if e:
                    channel.sendall(e)
                buf = ''
            if len(b) == 0:
                # print 'closing channel %d on empty recv' % channel.get_id()
                channel.close()
                return

    def stop(self):
        try:
            self.listensock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.listensock.close()
        except:
            pass
        self.listensock = None

    def __del__(self):
        self.stop()

    def check_auth_publickey(self, username, key):
        if self.user2key.get(username) == key:
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_channel_exec_request(self, channel, command):
        # print 'channel %d exec command %s' % (channel.get_id(), command)
        if command.startswith('scp'):
            if not self.enable_scp:
                return False
            self.scpchannelid2command[channel.get_id()] = command
            channel.sendall('\x00')
            t3 = threading.Thread(target=self.scp_session_thread, args=(channel,))
            t3.setDaemon(True)
            t3.start()
        else:
            o, e, ret = self.fake_device.do_command(command)
            if o:
                channel.sendall(o)
            if e:
                channel.sendall_stderr(e)
            channel.send_exit_status(ret)
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # print 'pty request channel %d' % channel.get_id()
        return True

    def check_channel_env_request(self, channel, name, value):
        # print 'env request channel %d' % channel.get_id()
        return True

    def check_channel_shell_request(self, channel):
        # print 'shell request %d' % channel.get_id()
        t3 = threading.Thread(target=self.session_thread, args=(channel,))
        t3.setDaemon(True)
        t3.start()
        return True

    def check_auth_password(self, username, password):
        # print 'check auth'
        if self.user2password.get(username) == password:
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_channel_subsystem_request(self, channel, name):
        # print 'subsystem request channel %d %s' % (channel.get_id(), name)
        return super(SSHServer, self).check_channel_subsystem_request(channel, name)

    def get_allowed_auths(self, username):
        if self.user2password:
            if self.user2key:
                return "password,publickey"
            else:
                return "password"
        else:
            if self.user2key:
                return "publickey"
            else:
                return ""

    def check_channel_request(self, kind, chanid):
        # print 'channel request kind="%s" channel %d' % (kind, chanid)
        return paramiko.OPEN_SUCCEEDED


class TestSshSession(TestCase):

    def setUp(self):
        self._username = 'user'
        self._password = 'pass'
        self._hostname = 'hostname'
        self._port = 22
        self._on_session_start = Mock()

    @patch('cloudshell.cli.session.ssh_session.ExpectSession')
    @patch('cloudshell.cli.session.ssh_session.ConnectionParams')
    def test_init_attributes(self, connection_params, expect_session):
        self._instance = SSHSession(self._hostname, self._username, self._password, port=self._port,
                                    on_session_start=self._on_session_start)
        mandatory_attributes = ['username', '_handler', '_current_channel', 'password', '_buffer_size']
        self.assertEqual(len(set(mandatory_attributes).difference(set(self._instance.__dict__.keys()))), 0)

    @patch('cloudshell.cli.session.ssh_session.ExpectSession')
    def test_eq(self, expect_session):
        self._instance = SSHSession(self._hostname, self._username, self._password, port=self._port,
                                    on_session_start=self._on_session_start)
        self.assertTrue(
            self._instance.__eq__(SSHSession(self._hostname, self._username, self._password, port=self._port,
                                             on_session_start=self._on_session_start)))
        self.assertFalse(
            self._instance.__eq__(SSHSession(self._hostname, 'incorrect_username', self._password, port=self._port,
                                             on_session_start=self._on_session_start)))
        self.assertFalse(
            self._instance.__eq__(SSHSession(self._hostname, self._username, 'incorrect_password', port=self._port,
                                             on_session_start=self._on_session_start)))

    def test_connect_simple(self):
        pkey = paramiko.RSAKey.from_private_key(StringIO(KEY_WITHOUT_PASSPHRASE))  # unused
        server = SSHServer(user2key={'user-1', pkey}, user2password={'user0': 'password0'})
        self._instance = SSHSession('127.0.0.1',
                                    'user0', 'password0',
                                    port=server.port,
                                    on_session_start=self._on_session_start)
        self._instance.connect('>', logger=Mock())
        self._instance.hardware_expect('ls', '>', Mock())

    def test_connect_timeout(self):
        self._instance = SSHSession('bad_host', 'user1', 'password1', on_session_start=self._on_session_start)
        with self.assertRaises(SSHSessionException):
            self._instance.connect('>', logger=Mock())

    def test_username_password(self):
        server = SSHServer(user2password={'user1': 'password1'})

        self._instance = SSHSession('127.0.0.1',
                                    'user1', 'password1',
                                    port=server.port,
                                    on_session_start=self._on_session_start)
        self._instance.connect('>', logger=Mock())
        self._instance.hardware_expect('ls', '>', Mock())

    def test_enable_exit(self):
        server = SSHServer(user2password={'user1': 'password1'})

        self._instance = SSHSession('127.0.0.1',
                                    'user1', 'password1',
                                    port=server.port,
                                    on_session_start=self._on_session_start)
        self._instance.connect('>', logger=Mock())
        o = self._instance.hardware_expect('ls', '>', Mock())
        self.assertTrue('[prompt]' in o)
        o = self._instance.hardware_expect('enable', '>', Mock())
        self.assertTrue('[enable]' in o)
        o = self._instance.hardware_expect('ls', '>', Mock())
        self.assertTrue('[enable]' in o)
        o = self._instance.hardware_expect('exit', '>', Mock())
        self.assertTrue('[prompt]' in o)
        o = self._instance.hardware_expect('ls', '>', Mock())
        self.assertTrue('[prompt]' in o)

    def test_rsa_without_passphrase(self):
        pkey = paramiko.RSAKey.from_private_key(StringIO(KEY_WITHOUT_PASSPHRASE))
        server = SSHServer(user2key={'user2': pkey})

        self._instance = SSHSession('127.0.0.1',
                                    'user2', '',
                                    port=server.port,
                                    on_session_start=self._on_session_start,
                                    rsa_key_string=KEY_WITHOUT_PASSPHRASE)
        self._instance.connect('>', logger=Mock())
        self._instance.hardware_expect('ls', '>', Mock())

    def test_rsa_with_good_passphrase(self):
        pkey = paramiko.RSAKey.from_private_key(StringIO(KEY_WITH_PASSPHRASE), password=KEY_PASSPHRASE)

        server = SSHServer(user2key={'user4': pkey})

        self._instance = SSHSession('127.0.0.1',
                                    'user4', '',
                                    port=server.port,
                                    on_session_start=self._on_session_start,
                                    rsa_key_string=KEY_WITH_PASSPHRASE,
                                    rsa_key_passphrase=KEY_PASSPHRASE)
        self._instance.connect('>', logger=Mock())
        self._instance.hardware_expect('ls', '>', Mock())

    def test_rsa_with_missing_passphrase(self):
        with self.assertRaises(PasswordRequiredException):
            self._instance = SSHSession('127.0.0.1',
                                        'user4', '',
                                        port=12345,
                                        on_session_start=self._on_session_start,
                                        rsa_key_string=KEY_WITH_PASSPHRASE)
            self._instance.connect('>', logger=Mock())
            self._instance.hardware_expect('ls', '>', Mock())

    def test_rsa_with_bad_passphrase(self):
        with self.assertRaises(SSHException):
            self._instance = SSHSession('127.0.0.1', 'user5', '',
                                        port=12345,
                                        on_session_start=self._on_session_start,
                                        rsa_key_string=KEY_WITH_PASSPHRASE,
                                        rsa_key_passphrase='bad passphrase')
            self._instance.connect('>', logger=Mock())
            self._instance.hardware_expect('ls', '>', Mock())


