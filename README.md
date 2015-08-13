# disposable-consul
Disposable Consul - Helper for unit testing with Consul


### Usage
```python
import unittest
import consul
from disposable_consul import DisposableConsul

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # Fire up a local consul server (by default will search for the "consul" binary in path)
        self.consul_server = DisposableConsul()
        self.consul_server.start()
        self.client = consul.Consul(port=self.consul_server.http_port)

    def tearDown(self):
        self.consul_server.stop()

    def test_123(self):
        # write code with you consul client
```
