import sys

from autobahn.twisted.websocket import WebSocketServerFactory
from hendrix.contrib.async.messaging import hxdispatcher
from hendrix.deploy.base import HendrixDeploy
from hendrix.experience import hey_joe
from hendrix.facilities.resources import NamedResource
from twisted.python import log

message_resource = NamedResource('hendrix-demo')

from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory


class TelnetToWebsocket(TelnetProtocol):
    def dataReceived(self, data):
        hxdispatcher.send('noodly_messages', data)


telnet_server_factory = ServerFactory()
telnet_server_factory.protocol = lambda: TelnetTransport(TelnetToWebsocket)

deployer = HendrixDeploy(options={'wsgi': 'hendrix_demo.wsgi.application'})
deployer.resources.append(message_resource)

log.startLogging(sys.stdout)

factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
factory.protocol = hey_joe.MyServerProtocol

deployer.reactor.listenTCP(9000, factory)

deployer.reactor.listenTCP(6565, telnet_server_factory)
deployer.run()
