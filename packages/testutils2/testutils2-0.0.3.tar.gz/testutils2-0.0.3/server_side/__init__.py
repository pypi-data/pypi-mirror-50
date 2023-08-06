import sys

sys.path.append('contracts/')
sys.path.append('accounts/')

from web_server import WebServer

import account_rest
import contract_rest

webserver = WebServer()
webserver.init('config.json')

account_rest.register_rest_api()
contract_rest.register_rest_api()

webserver.run()