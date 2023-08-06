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

# This module implements XEP-0355 (Namespace delegation) to use SàT Pubsub as PEP service

from wokkel.subprotocols import XMPPHandler
from wokkel import pubsub
from wokkel import data_form
from wokkel import disco, iwokkel
from wokkel.iwokkel import IPubSubService
from wokkel import mam
from twisted.python import log
from twisted.words.protocols.jabber import jid, error
from twisted.words.protocols.jabber.xmlstream import toResponse
from twisted.words.xish import domish
from zope.interface import implements

DELEGATION_NS = 'urn:xmpp:delegation:1'
FORWARDED_NS = 'urn:xmpp:forward:0'
DELEGATION_ADV_XPATH = '/message/delegation[@xmlns="{}"]'.format(DELEGATION_NS)
DELEGATION_FWD_XPATH = '/iq[@type="set"]/delegation[@xmlns="{}"]/forwarded[@xmlns="{}"]'.format(DELEGATION_NS, FORWARDED_NS)

DELEGATION_MAIN_SEP = "::"
DELEGATION_BARE_SEP = ":bare:"

TO_HACK = ((IPubSubService, pubsub, "PubSubRequest"),
           (mam.IMAMService, mam, "MAMRequest"))


class InvalidStanza(Exception):
    pass


class DelegationsHandler(XMPPHandler):
    implements(iwokkel.IDisco)
    _service_hacked = False

    def __init__(self):
        super(DelegationsHandler, self).__init__()

    def _service_hack(self):
        """Patch the request classes of services to track delegated stanzas"""
        # XXX: we need to monkey patch to track origin of the stanza in PubSubRequest.
        #      As PubSubRequest from sat.tmp.wokkel.pubsub use _request_class while
        #      original wokkel.pubsub use directly pubsub.PubSubRequest, we need to
        #      check which version is used before monkeypatching
        for handler in self.parent.handlers:
            for service, module, default_base_cls in TO_HACK:
                if service.providedBy(handler):
                    if hasattr(handler, '_request_class'):
                        request_base_class = handler._request_class
                    else:
                        request_base_class = getattr(module, default_base_cls)

                    class RequestWithDelegation(request_base_class):
                        """A XxxRequest which put an indicator if the stanza comme from delegation"""

                        @classmethod
                        def fromElement(cls, element):
                            """Check if element comme from delegation, and set a delegated flags

                            delegated flag is either False, or it's a jid of the delegating server
                            the delegated flag must be set on element before use
                            """
                            try:
                                # __getattr__ is overriden in domish.Element, so we use __getattribute__
                                delegated = element.__getattribute__('delegated')
                            except AttributeError:
                                delegated = False
                            instance = cls.__base__.fromElement(element)
                            instance.delegated = delegated
                            return instance

                    if hasattr(handler, '_request_class'):
                        handler._request_class = RequestWithDelegation
                    else:
                        setattr(module, default_base_cls, RequestWithDelegation)
        DelegationsHandler._service_hacked = True

    def connectionInitialized(self):
        if not self._service_hacked:
            self._service_hack()
        self.xmlstream.addObserver(DELEGATION_ADV_XPATH, self.onAdvertise)
        self.xmlstream.addObserver(DELEGATION_FWD_XPATH, self._obsWrapper, 0, self.onForward)
        self._current_iqs = {} # dict of iq being handler by delegation
        self._xs_send = self.xmlstream.send
        self.xmlstream.send = self._sendHack

    def _sendHack(self, elt):
        """This method is called instead of xmlstream to control sending

        @param obj(domsish.Element, unicode, str): obj sent to real xmlstream
        """
        if isinstance(elt, domish.Element) and elt.name=='iq':
            try:
                id_ = elt.getAttribute('id')
                ori_iq, managed_entity = self._current_iqs[id_]
                if jid.JID(elt['to']) != managed_entity:
                    log.msg("IQ id conflict: the managed entity doesn't match (got {got} was expecting {expected})"
                            .format(got=jid.JID(elt['to']), expected=managed_entity))
                    raise KeyError
            except KeyError:
                # the iq is not a delegated one
                self._xs_send(elt)
            else:
                del self._current_iqs[id_]
                iq_result_elt = toResponse(ori_iq, 'result')
                fwd_elt = iq_result_elt.addElement('delegation', DELEGATION_NS).addElement('forwarded', FORWARDED_NS)
                fwd_elt.addChild(elt)
                elt.uri = elt.defaultUri = 'jabber:client'
                self._xs_send(iq_result_elt)
        else:
            self._xs_send(elt)

    def _obsWrapper(self, observer, stanza):
        """Wrapper to observer which catch StanzaError

        @param observer(callable): method to wrap
        """
        try:
            observer(stanza)
        except error.StanzaError as e:
            error_elt = e.toResponse(stanza)
            self._xs_send(error_elt)
        stanza.handled = True

    def onAdvertise(self, message):
        """Manage the <message/> advertising delegations"""
        delegation_elt = message.elements(DELEGATION_NS, 'delegation').next()
        delegated = {}
        for delegated_elt in delegation_elt.elements(DELEGATION_NS):
            try:
                if delegated_elt.name != 'delegated':
                    raise InvalidStanza(u'unexpected element {}'.format(delegated_elt.name))
                try:
                    namespace = delegated_elt['namespace']
                except KeyError:
                    raise InvalidStanza(u'was expecting a "namespace" attribute in delegated element')
                delegated[namespace] = []
                for attribute_elt in delegated_elt.elements(DELEGATION_NS, 'attribute'):
                    try:
                        delegated[namespace].append(attribute_elt["name"])
                    except KeyError:
                        raise InvalidStanza(u'was expecting a "name" attribute in attribute element')
            except InvalidStanza as e:
                log.msg("Invalid stanza received ({})".format(e))

        log.msg(u'delegations updated:\n{}'.format(
            u'\n'.join([u"    - namespace {}{}".format(ns,
            u"" if not attributes else u" with filtering on {} attribute(s)".format(
            u", ".join(attributes))) for ns, attributes in delegated.items()])))

        if not pubsub.NS_PUBSUB in delegated:
            log.msg(u"Didn't got pubsub delegation from server, can't act as a PEP service")

    def onForward(self, iq):
        """Manage forwarded iq

        @param iq(domish.Element): full delegation stanza
        """

        # FIXME: we use a hack supposing that our delegation come from hostname
        #        and we are a component named [name].hostname
        #        but we need to manage properly allowed servers
        # TODO: do proper origin security check
        _, allowed = iq['to'].split('.', 1)
        if jid.JID(iq['from']) != jid.JID(allowed):
            log.msg((u"SECURITY WARNING: forwarded stanza doesn't come from our server: {}"
                     .format(iq.toXml())).encode('utf-8'))
            raise error.StanzaError('not-allowed')

        try:
            fwd_iq = (iq.elements(DELEGATION_NS, 'delegation').next()
                      .elements(FORWARDED_NS, 'forwarded').next()
                      .elements('jabber:client', 'iq').next())
        except StopIteration:
            raise error.StanzaError('not-acceptable')

        managed_entity = jid.JID(fwd_iq['from'])

        self._current_iqs[fwd_iq['id']] = (iq, managed_entity)
        fwd_iq.delegated = True

        # we need a recipient in pubsub request for PEP
        # so we set "to" attribute if it doesn't exist
        if not fwd_iq.hasAttribute('to'):
            fwd_iq["to"] = jid.JID(fwd_iq["from"]).userhost()

        # we now inject the element in the stream
        self.xmlstream.dispatch(fwd_iq)

    def getDiscoInfo(self, requestor, target, nodeIdentifier=''):
        """Manage disco nesting

        This method looks for DiscoHandler in sibling handlers and use it to
        collect main disco infos. It then filters by delegated namespace and return it.
        An identity is added for PEP if pubsub namespace is requested.

        The same features/identities are returned for main and bare nodes
        """
        if not nodeIdentifier.startswith(DELEGATION_NS):
            return []

        try:
            _, namespace = nodeIdentifier.split(DELEGATION_MAIN_SEP, 1)
        except ValueError:
            try:
                _, namespace = nodeIdentifier.split(DELEGATION_BARE_SEP, 1)
            except ValueError:
                log.msg("Unexpected disco node: {}".format(nodeIdentifier))
                raise error.StanzaError('not-acceptable')

        if not namespace:
            log.msg("No namespace found in node {}".format(nodeIdentifier))
            return []

        if namespace.startswith(pubsub.NS_PUBSUB):
            # pubsub use several namespaces starting with NS_PUBSUB (e.g. http://jabber.org/protocol/pubsub#owner)
            # we return the same disco for all of them
            namespace = pubsub.NS_PUBSUB

        def gotInfos(infos):
            ns_features = []
            for info in infos:
                if isinstance(info, disco.DiscoFeature) and info.startswith(namespace):
                    ns_features.append(info)
                elif (isinstance(info, data_form.Form) and info.formNamespace
                    and info.formNamespace.startwith(namespace)):
                    # extensions management (XEP-0128)
                    ns_features.append(info)

            if namespace == pubsub.NS_PUBSUB:
                ns_features.append(disco.DiscoIdentity('pubsub', 'pep'))

            return ns_features

        for handler in self.parent.handlers:
            if isinstance(handler, disco.DiscoHandler):
                break

        if not isinstance(handler, disco.DiscoHandler):
            log.err("Can't find DiscoHandler")
            return []

        d = handler.info(requestor, target, '')
        d.addCallback(gotInfos)
        return d

    def getDiscoItems(self, requestor, target, nodeIdentifier=''):
        return []


# we monkeypatch DiscoHandler to add delegation informations
def _onDiscoItems(self, iq):
    request = disco._DiscoRequest.fromElement(iq)
    # it's really ugly to attach pep data to recipient
    # but we don't have many options
    request.recipient.pep = iq.delegated

    def toResponse(items):
        response = disco.DiscoItems()
        response.nodeIdentifier = request.nodeIdentifier

        for item in items:
            response.append(item)

        return response.toElement()

    d = self.items(request.sender, request.recipient,
                   request.nodeIdentifier)
    d.addCallback(toResponse)
    return d


disco.DiscoHandler._onDiscoItems = _onDiscoItems
