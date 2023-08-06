#!/usr/bin/python
#-*- coding: utf-8 -*-

# Copyright (c) 2019 Jérôme Poisson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Pubsub Admin experimental protocol implementation

"""

from zope.interface import implements
from twisted.python import log
from twisted.internet import defer
from twisted.words.protocols.jabber import jid, error as jabber_error, xmlstream
from sat_pubsub import error
from wokkel.subprotocols import XMPPHandler
from wokkel import disco, iwokkel, pubsub

NS_PUBSUB_ADMIN = u"https://salut-a-toi.org/spec/pubsub_admin:0"
ADMIN_REQUEST = '/iq[@type="set"]/admin[@xmlns="{}"]'.format(NS_PUBSUB_ADMIN)


class PubsubAdminHandler(XMPPHandler):
    implements(iwokkel.IDisco)

    def __init__(self, backend):
        super(PubsubAdminHandler, self).__init__()
        self.backend = backend

    def connectionInitialized(self):
        self.xmlstream.addObserver(ADMIN_REQUEST, self.onAdminRequest)

    def sendError(self, iq_elt, condition=u'bad-request'):
        stanza_error = jabber_error.StanzaError(condition)
        iq_error = stanza_error.toResponse(iq_elt)
        self.parent.xmlstream.send(iq_error)

    @defer.inlineCallbacks
    def onAdminRequest(self, iq_elt):
        """Pubsub Admin request received"""
        iq_elt.handled = True
        try:
            pep = bool(iq_elt.delegated)
        except AttributeError:
            pep = False

        # is the sender really an admin?
        admins = self.backend.config[u'admins_jids_list']
        from_jid = jid.JID(iq_elt[u'from'])
        if from_jid.userhostJID() not in admins:
            log.msg("WARNING: admin request done by non admin entity {from_jid}"
                .format(from_jid=from_jid.full()))
            self.sendError(iq_elt, u'forbidden')
            return

        # alright, we can proceed
        recipient = jid.JID(iq_elt[u'to'])
        admin_elt = iq_elt.admin
        try:
            pubsub_elt = next(admin_elt.elements(pubsub.NS_PUBSUB, u'pubsub'))
            publish_elt = next(pubsub_elt.elements(pubsub.NS_PUBSUB, u'publish'))
        except StopIteration:
            self.sendError(iq_elt)
            return
        try:
            node = publish_elt[u'node']
        except KeyError:
            self.sendError(iq_elt)
            return

        # we prepare the result IQ request, we will fill it with item ids
        iq_result_elt = xmlstream.toResponse(iq_elt, u'result')
        result_admin_elt = iq_result_elt.addElement((NS_PUBSUB_ADMIN, u'admin'))
        result_pubsub_elt = result_admin_elt.addElement((pubsub.NS_PUBSUB, u'pubsub'))
        result_publish_elt = result_pubsub_elt.addElement(u'publish')
        result_publish_elt[u'node'] = node

        # now we can send the items
        for item in publish_elt.elements(pubsub.NS_PUBSUB, u'item'):
            try:
                requestor = jid.JID(item.attributes.pop(u'publisher'))
            except Exception as e:
                log.msg(u"WARNING: invalid jid in publisher ({requestor}): {msg}"
                    .format(requestor=requestor, msg=e))
                self.sendError(iq_elt)
                return
            except KeyError:
                requestor = from_jid

            # we don't use a DeferredList because we want to be sure that
            # each request is done in order
            try:
                payload = yield self.backend.publish(
                    nodeIdentifier=node,
                    items=[item],
                    requestor=requestor,
                    pep=pep,
                    recipient=recipient)
            except (error.Forbidden, error.ItemForbidden):
                __import__('pudb').set_trace()
                self.sendError(iq_elt, u"forbidden")
                return
            except Exception as e:
                self.sendError(iq_elt, u"internal-server-error")
                log.msg(u"INTERNAL ERROR: {msg}".format(msg=e))
                return

            result_item_elt = result_publish_elt.addElement(u'item')
            # either the id was given and it is available in item
            # either it's a new item, and we can retrieve it from return payload
            try:
                result_item_elt[u'id'] = item[u'id']
            except KeyError:
                result_item_elt = payload.publish.item[u'id']

        self.xmlstream.send(iq_result_elt)

    def getDiscoInfo(self, requestor, service, nodeIdentifier=''):
        return [disco.DiscoFeature(NS_PUBSUB_ADMIN)]

    def getDiscoItems(self, requestor, service, nodeIdentifier=''):
        return []
