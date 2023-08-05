### Socket Wait

Basic utility to block until a connection is a recieved on a socket.

### Usage

Works with python 2.7+.

Install with pip:

```
pip install socket-wait
```

This adds a new CLI tool:

```
socket_wait 9009
```

This will bind to port 9009 and block until a connection is received, like so:

```
nc -z localhost 9009
```

### Why?

Inter-process communication. TCP allows a quick and dependency-free way for one process to alert another that
it is ready, or has completed, or any number of things. I use it in docker-compose apps which require some sort of loading to occur
before the service is ready (like loading some data to a database which the process will use). This allows the service performing the loading to call back to
the waiting process (waiting using this tool) to let it know that it can proceed.