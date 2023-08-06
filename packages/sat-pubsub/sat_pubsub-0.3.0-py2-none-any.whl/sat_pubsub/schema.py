#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 Jérôme Poisson


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# ---

# This module implements node schema

from twisted.words.protocols.jabber import jid
from twisted.words.xish import domish
from wokkel import disco, iwokkel
from wokkel.iwokkel import IPubSubService
from wokkel.subprotocols import XMPPHandler, IQHandlerMixin
from wokkel import data_form, pubsub
from zope.interface import implements
from sat_pubsub import const

QUERY_SCHEMA = "/pubsub[@xmlns='" + const.NS_SCHEMA + "']"


class SchemaHandler(XMPPHandler, IQHandlerMixin):
    implements(iwokkel.IDisco)
    iqHandlers = {"/iq[@type='get']" + QUERY_SCHEMA: 'onSchemaGet',
                  "/iq[@type='set']" + QUERY_SCHEMA: 'onSchemaSet'}

    def __init__(self):
        super(SchemaHandler, self).__init__()
        self.pubsub_service = None

    def connectionInitialized(self):
        for handler in self.parent.handlers:
            if IPubSubService.providedBy(handler):
                self.pubsub_service = handler
                break
        self.backend = self.parent.parent.getServiceNamed('backend')
        self.xmlstream.addObserver("/iq[@type='get' or @type='set']" + QUERY_SCHEMA, self.handleRequest)

    def _getNodeSchemaCb(self, x_elt, nodeIdentifier):
        schema_elt = domish.Element((const.NS_SCHEMA, 'schema'))
        schema_elt['node'] = nodeIdentifier
        if x_elt is not None:
            assert x_elt.uri == u'jabber:x:data'
            schema_elt.addChild(x_elt)
        return schema_elt

    def onSchemaGet(self, iq_elt):
        try:
            schema_elt = next(iq_elt.pubsub.elements(const.NS_SCHEMA, 'schema'))
            nodeIdentifier = schema_elt['node']
        except StopIteration:
            raise pubsub.BadRequest(text='missing schema element')
        except KeyError:
            raise pubsub.BadRequest(text='missing node')
        pep = iq_elt.delegated
        recipient = jid.JID(iq_elt['to'])
        d = self.backend.getNodeSchema(nodeIdentifier,
                                       pep,
                                       recipient)
        d.addCallback(self._getNodeSchemaCb, nodeIdentifier)
        return d.addErrback(self.pubsub_service.resource._mapErrors)

    def onSchemaSet(self, iq_elt):
        try:
            schema_elt = next(iq_elt.pubsub.elements(const.NS_SCHEMA, 'schema'))
            nodeIdentifier = schema_elt['node']
        except StopIteration:
            raise pubsub.BadRequest(text='missing schema element')
        except KeyError:
            raise pubsub.BadRequest(text='missing node')
        requestor = jid.JID(iq_elt['from'])
        pep = iq_elt.delegated
        recipient = jid.JID(iq_elt['to'])
        try:
            x_elt = next(schema_elt.elements(data_form.NS_X_DATA, u'x'))
        except StopIteration:
            # no schema form has been found
            x_elt = None
        d = self.backend.setNodeSchema(nodeIdentifier,
                                       x_elt,
                                       requestor,
                                       pep,
                                       recipient)
        return d.addErrback(self.pubsub_service.resource._mapErrors)

    def getDiscoInfo(self, requestor, service, nodeIdentifier=''):
        return [disco.DiscoFeature(const.NS_SCHEMA)]

    def getDiscoItems(self, requestor, service, nodeIdentifier=''):
        return []
