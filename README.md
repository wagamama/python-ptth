# python-ptth
Reverse HTTP (PTTH) client implementation according to [Second Life Wiki](http://wiki.secondlife.com/wiki/Reverse_HTTP)

# Installation
```shell
pip install ptth
```

# Example
```python
import ptth

class MyHandler(ptth.Handler):
    def ready_to_handle(self):
        ''' ready to accept ptth request '''
        pass

    def handle_request(self, request):
        '''
        request is type of ptth.Request
        process the request and then return ptth.Response
        '''
        return ptth.Response(200)

    def handle_error(self, error):
        ''' handle occurred error '''
        pass

    def handle_close(self):
        ''' ptth service is closed '''
        pass

h = MyHandler()
session = ptth.Session(h)
session.serve('http://host.support.ptth/')

''' doing something '''

session.close()
```
