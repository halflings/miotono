import requests
import json


class RpcException(Exception):
    pass


class JsonRpcClient(object):

    def __init__(self, url):
        self.url = url

    def call(self, method, *args):
        payload = dict(method=method, params=args, jsonrpc='1.0', id=0)
        response = requests.post(self.url,
                                 data=json.dumps(payload),
                                 headers={'content-type': 'application/json'})
        if not response.ok or response.headers.get('content-type') != 'application/json':
            raise RpcException("Server-side error: '{}'".format(response.content))
        response_json = response.json()
        if 'error' in response_json:
            raise RpcException("Error processing the RPC request: '{}'".format(
                response_json['error']))
        return response_json['result']


def main():
    rpc = JsonRpcClient("http://localhost:4000/jsonrpc")
    response = rpc.call('echo', 'echome!')
    assert response == 'echome!'


if __name__ == "__main__":
    main()
