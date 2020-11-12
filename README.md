# replicated-log
Distributed systems course @ UCU



### Prerequisites

Using Python3.8

If necessary, upgrade your version of `pip`:

```sh
$ python -m pip install --upgrade pip
```

If you cannot upgrade `pip` due to a system-owned installation, you can
run the example in a virtualenv:

```sh
$ python -m pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip
```

#### gRPC

Install gRPC:

```sh
$ python -m pip install grpcio
```

Or, to install it system wide:

```sh
$ sudo python -m pip install grpcio
```

On El Capitan OSX, you may get the following error:

```sh
$ OSError: [Errno 1] Operation not permitted: '/tmp/pip-qwTLbI-uninstall/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info'
```

You can work around this using:

```sh
$ python -m pip install grpcio --ignore-installed
```

#### gRPC tools

Python's gRPC tools include the protocol buffer compiler `protoc` and the
special plugin for generating server and client code from `.proto` service
definitions. For the first part of our quick-start example, we've already
generated the server and client stubs from
[helloworld.proto](https://github.com/grpc/grpc/tree/{{< param grpc_vers.core >}}/examples/protos/helloworld.proto),
but you'll need the tools for the rest of our quick start, as well as later
tutorials and your own projects.

To install gRPC tools, run:

```sh
$ python -m pip install grpcio-tools
```

Generate gRPC service code from proto file.
```bash
python -m grpc_tools.protoc --proto_path=../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto
```