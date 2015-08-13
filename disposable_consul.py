from __future__ import absolute_import
from subprocess import Popen, PIPE

import tempfile
import shutil
import socket
import os
import json


class DisposableConsul(object):
    DEFAULT_CONSUL_BIN = 'consul'

    def __init__(self, consul_bin=DEFAULT_CONSUL_BIN):
        self.consul_bin = consul_bin
        self.temp_dir = None
        self.consul = None
        self.config = None

    @staticmethod
    def find_unused_port():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[-1]
        sock.close()
        return port

    def start(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = self.generate_config()
        config_file = os.path.join(self.temp_dir, 'config.json')
        with open(config_file, 'w') as f:
            json.dump(self.config, f)
        self.consul = Popen([self.consul_bin, 'agent', '-server',
                             '-data-dir', self.temp_dir,
                             '-bootstrap-expect', '1',
                             '-config-file', config_file], stdout=PIPE, stderr=PIPE)
        while True:
            line = self.consul.stdout.readline().strip()
            if 'New leader elected' in line:
                break

    def generate_config(self):
        return {
            'ports': {
                k: self.find_unused_port() for k in
                ('dns', 'http', 'https', 'rpc', 'serf_lan', 'serf_wan', 'server')
            }
        }

    def stop(self):
        self.consul.terminate()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @property
    def http_port(self):
        return self.config['ports']['http']