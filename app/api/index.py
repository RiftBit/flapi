from app import jsonrpc


def check_auth(username, password):
    if username == password:
        return True
    else:
        return False


@jsonrpc.method('Index.index', authenticated=check_auth)
def index():
    return u'Welcome to Flask JSON-RPC'


@jsonrpc.method('Index.echo(name=str) -> str', validate=True, authenticated=check_auth)
def echo(name='Flask JSON-RPC'):
    return u'Hello {0}'.format(name)


@jsonrpc.method('Index.hello')
def hello(name):
    return u'Hello {0}'.format(name)


@jsonrpc.method('Index.helloDefaultArgs')
def hello_default_args(string='Flask JSON-RPC'):
    return u'We salute you {0}'.format(string)


@jsonrpc.method('Index.argsValidateJSONMode(a1=Number, a2=String, a3=Boolean, a4=Array, a5=Object) -> Object')
def args_validate_json_mode(a1, a2, a3, a4, a5):
    return u'Number: {0}, String: {1}, Boolean: {2}, Array: {3}, Object: {4}'.format(a1, a2, a3, a4, a5)


@jsonrpc.method('Index.argsValidatePythonMode(a1=int, a2=str, a3=bool, a4=list, a5=dict) -> object')
def args_validate_python_mode(a1, a2, a3, a4, a5):
    return u'int: {0}, str: {1}, bool: {2}, list: {3}, dict: {4}'.format(a1, a2, a3, a4, a5)


@jsonrpc.method('Index.notify')
def notify(string):
    pass


@jsonrpc.method('Index.fails')
def fails(string):
    raise ValueError