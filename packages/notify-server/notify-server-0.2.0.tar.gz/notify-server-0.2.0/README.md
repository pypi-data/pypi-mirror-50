# Notify Server

*A simple command line event server*

This is a server and client interface to send and receive
notifications via cli or Python over a socket.

## Usage

Start the server:
```bash
notify-server localhost:9080
```
Subscribe to an event via cli:
```bash
notify-client localhost:9000 receive terminal_event
```

Subscribe to an event via Python:
```python
from notify_cli import NotifyClient
client = NotifyClient('localhost', 9000)
client.subscribe('python_event', lambda event: print('Event:', event))

while True:
    sleep(1)
```

Send an event via cli:
```bash
notify-client localhost:9000 send python_event 'hello, from the cli'
```

Send an event via Python:
```python
from notify_cli import NotifyClient
client = NotifyClient('localhost', 9000)
client.send('terminal_event', 'hello from python')

while True:
    sleep(1)
```

## Installation

Installation:

```bash
pip3 install notify-server
```

If you are using the client code in a project you only need:
```bash
pip3 install notify-client
```
