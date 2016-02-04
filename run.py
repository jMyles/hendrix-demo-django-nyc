from hendrix.contrib.async.messaging import hxdispatcher
from hendrix.deploy.base import HendrixDeploy

from txsockjs.factory import SockJSResource
from hendrix.contrib.async.resources import MessageHandlerProtocol
from hendrix.facilities.resources import NamedResource
from twisted.internet.protocol import Factory

message_resource = NamedResource('hendrix-demo')
message_resource.putChild('messages', SockJSResource(Factory.forProtocol(MessageHandlerProtocol)))



from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from twisted.internet.protocol import ServerFactory


class TelnetToWebsocket(TelnetProtocol):

    def dataReceived(self, data):
        hxdispatcher.send('noodly_messages', data)

telnet_server_factory = ServerFactory()
telnet_server_factory.protocol = lambda: TelnetTransport(TelnetToWebsocket)

deployer = HendrixDeploy(options={'wsgi': 'hendrix_demo.wsgi.application'})
deployer.resources.append(message_resource)
deployer.reactor.listenTCP(6565, telnet_server_factory)
deployer.run()