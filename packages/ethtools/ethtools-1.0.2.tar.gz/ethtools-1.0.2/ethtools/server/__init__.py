import sys

from web_server import WebServer

from accounts.account_rest import register_rest_api as accounts_rest
from contracts.contract_rest import register_rest_api as contracts_rest

class EthServer:
    def __init__(self, config_path):
        webserver = WebServer()
        webserver.init(config_path)
        accounts_rest()
        contracts_rest()
        webserver.run()
