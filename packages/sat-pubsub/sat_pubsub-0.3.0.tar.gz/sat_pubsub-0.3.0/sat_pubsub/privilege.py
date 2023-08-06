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

# This module implements XEP-0356 (Privileged Entity) to manage rosters, messages and presences

from wokkel import xmppim
from wokkel.compat import IQ
from wokkel import pubsub
from wokkel import disco
from wokkel.iwokkel import IPubSubService
from twisted.python import log
from twisted.python import failure
from twisted.internet import defer
from twisted.words.xish import domish
from twisted.words.protocols.jabber import jid
import time

FORWARDED_NS = 'urn:xmpp:forward:0'
PRIV_ENT_NS = 'urn:xmpp:privilege:1'
PRIV_ENT_ADV_XPATH = '/message/privilege[@xmlns="{}"]'.format(PRIV_ENT_NS)
ROSTER_NS = 'jabber:iq:roster'
PERM_ROSTER = 'roster'
PERM_MESSAGE = 'message'
PERM_PRESENCE = 'presence'
ALLOWED_ROSTER = ('none', 'get', 'set', 'both')
ALLOWED_MESSAGE = ('none', 'outgoing')
ALLOWED_PRESENCE = ('none', 'managed_entity', 'roster')
TO_CHECK = {PERM_ROSTER:ALLOWED_ROSTER, PERM_MESSAGE:ALLOWED_MESSAGE, PERM_PRESENCE:ALLOWED_PRESENCE}


class InvalidStanza(Exception):
    pass

class NotAllowedError(Exception):
    pass

class PrivilegesHandler(disco.DiscoClientProtocol):
    #FIXME: need to manage updates, and database sync
    #TODO: cache

    def __init__(self, service_jid):
        super(PrivilegesHandler, self).__init__()
        self._permissions = {PERM_ROSTER: 'none',
                             PERM_MESSAGE: 'none',
                             PERM_PRESENCE: 'none'}
        self._pubsub_service = None
        self._backend = None
        # FIXME: we use a hack supposing that our privilege come from hostname
        #        and we are a component named [name].hostname
        #        but we need to manage properly server
        # TODO: do proper server handling
        self.server_jid = jid.JID(service_jid.host.split('.', 1)[1])
        self.caps_map = {}  # key: bare jid, value: dict of resources with caps hash
        self.hash_map = {}  # key: (hash,version), value: dict with DiscoInfo instance (infos) and nodes to notify (notify)
        self.roster_cache = {}  # key: jid, value: dict with "timestamp" and "roster"
        self.presence_map = {}  # inverted roster: key: jid, value: set of entities who has this jid in roster (with presence of "from" or "both")
        self.server = None

    @property
    def permissions(self):
        return self._permissions

    def connectionInitialized(self):
        for handler in self.parent.handlers:
            if IPubSubService.providedBy(handler):
                self._pubsub_service = handler
                break
        self._backend = self.parent.parent.getServiceNamed('backend')
        self.xmlstream.addObserver(PRIV_ENT_ADV_XPATH, self.onAdvertise)
        self.xmlstream.addObserver('/presence', self.onPresence)

    def onAdvertise(self, message):
        """Managage the <message/> advertising privileges

        self._permissions will be updated according to advertised privileged
        """
        privilege_elt = message.elements(PRIV_ENT_NS, 'privilege').next()
        for perm_elt in privilege_elt.elements(PRIV_ENT_NS):
            try:
                if perm_elt.name != 'perm':
                    raise InvalidStanza(u'unexpected element {}'.format(perm_elt.name))
                perm_access = perm_elt['access']
                perm_type = perm_elt['type']
                try:
                    if perm_type not in TO_CHECK[perm_access]:
                        raise InvalidStanza(u'bad type [{}] for permission {}'.format(perm_type, perm_access))
                except KeyError:
                    raise InvalidStanza(u'bad permission [{}]'.format(perm_access))
            except InvalidStanza as e:
                log.msg("Invalid stanza received ({}), setting permission to none".format(e))
                for perm in self._permissions:
                    self._permissions[perm] = 'none'
                break

            self._permissions[perm_access] = perm_type or 'none'

        log.msg('Privileges updated: roster={roster}, message={message}, presence={presence}'.format(**self._permissions))

    ## roster ##

    def getRoster(self, to_jid):
        """
        Retrieve contact list.

        @return: Roster as a mapping from L{JID} to L{RosterItem}.
        @rtype: L{twisted.internet.defer.Deferred}
        """
        # TODO: cache results
        if self._permissions[PERM_ROSTER] not in ('get', 'both'):
            log.msg("WARNING: permission not allowed to get roster")
            raise failure.Failure(NotAllowedError('roster get is not allowed'))

        def processRoster(result):
            roster = {}
            for element in result.query.elements(ROSTER_NS, 'item'):
                item = xmppim.RosterItem.fromElement(element)
                roster[item.entity] = item

            return roster

        iq = IQ(self.xmlstream, 'get')
        iq.addElement((ROSTER_NS, 'query'))
        iq["to"] = to_jid.userhost()
        d = iq.send()
        d.addCallback(processRoster)
        return d

    def _isSubscribedFrom(self, roster, entity, roster_owner_jid):
        try:
            return roster[entity.userhostJID()].subscriptionFrom
        except KeyError:
            return False

    def isSubscribedFrom(self, entity, roster_owner_jid):
        """Check if entity has presence subscription from roster_owner_jid

        @param entity(jid.JID): entity to check subscription to
        @param roster_owner_jid(jid.JID): owner of the roster to check
        @return D(bool): True if entity has a subscription from roster_owner_jid
        """
        d = self.getRoster(roster_owner_jid)
        d.addCallback(self._isSubscribedFrom, entity, roster_owner_jid)
        return d

    ## message ##

    def sendMessage(self, priv_message, to_jid=None):
        """Send privileged message (in the name of the server)

        @param priv_message(domish.Element): privileged message
        @param to_jid(jid.JID, None): main message destinee
            None to use our own server
        """
        if self._permissions[PERM_MESSAGE] not in ('outgoing',):
            log.msg("WARNING: permission not allowed to send privileged messages")
            raise failure.Failure(NotAllowedError('privileged messages are not allowed'))

        main_message = domish.Element((None, "message"))
        if to_jid is None:
            to_jid = self.server_jid
        main_message['to'] = to_jid.full()
        privilege_elt = main_message.addElement((PRIV_ENT_NS, 'privilege'))
        forwarded_elt = privilege_elt.addElement((FORWARDED_NS, 'forwarded'))
        priv_message['xmlns'] = 'jabber:client'
        forwarded_elt.addChild(priv_message)
        self.send(main_message)

    def notifyPublish(self, pep_jid, nodeIdentifier, notifications):
        """Do notifications using privileges"""
        for subscriber, subscriptions, items in notifications:
            message = self._pubsub_service._createNotification('items', pep_jid,
                                               nodeIdentifier, subscriber,
                                               subscriptions)
            for item in items:
                item.uri = pubsub.NS_PUBSUB_EVENT
                message.event.items.addChild(item)
            self.sendMessage(message)


    def notifyRetract(self, pep_jid, nodeIdentifier, notifications):
        for subscriber, subscriptions, items in notifications:
            message = self._pubsub_service._createNotification('items', pep_jid,
                                               nodeIdentifier, subscriber,
                                               subscriptions)
            for item in items:
                retract = domish.Element((None, "retract"))
                retract['id'] = item['id']
                message.event.items.addChild(retract)
            self.sendMessage(message)


    # def notifyDelete(self, service, nodeIdentifier, subscribers,
    #                        redirectURI=None):
    #     # TODO
    #     for subscriber in subscribers:
    #         message = self._createNotification('delete', service,
    #                                            nodeIdentifier,
    #                                            subscriber)
    #         if redirectURI:
    #             redirect = message.event.delete.addElement('redirect')
    #             redirect['uri'] = redirectURI
    #         self.send(message)


    ## presence ##

    @defer.inlineCallbacks
    def onPresence(self, presence_elt):
        if self.server is None:
            # FIXME: we use a hack supposing that our delegation come from hostname
            #        and we are a component named [name].hostname
            #        but we need to manage properly allowed servers
            # TODO: do proper origin security check
            _, self.server = presence_elt['to'].split('.', 1)
        from_jid = jid.JID(presence_elt['from'])
        from_jid_bare = from_jid.userhostJID()
        if from_jid.host == self.server and from_jid_bare not in self.roster_cache:
            roster = yield self.getRoster(from_jid_bare)
            timestamp = time.time()
            self.roster_cache[from_jid_bare] = {'timestamp': timestamp,
                                                'roster': roster,
                                                }
            for roster_jid, roster_item in roster.iteritems():
                if roster_item.subscriptionFrom:
                    self.presence_map.setdefault(roster_jid, set()).add(from_jid_bare)

        presence_type = presence_elt.getAttribute('type')
        if presence_type != "unavailable":
            # new resource available, we check entity capabilities
            try:
                c_elt = next(presence_elt.elements('http://jabber.org/protocol/caps', 'c'))
                hash_ = c_elt['hash']
                ver = c_elt['ver']
            except (StopIteration, KeyError):
                # no capabilities, we don't go further
                return

            # FIXME: hash is not checked (cf. XEP-0115)
            disco_tuple = (hash_, ver)

            if disco_tuple not in self.hash_map:
                # first time we se this hash, what is behind it?
                infos = yield self.requestInfo(from_jid)
                self.hash_map[disco_tuple] = {
                    'notify': {f[:-7] for f in infos.features if f.endswith('+notify')},
                    'infos': infos
                    }

            # jid_caps must be filled only after hash_map is set, to be sure that
            # the hash data is available in getAutoSubscribers
            jid_caps = self.caps_map.setdefault(from_jid_bare, {})
            if from_jid.resource not in jid_caps:
                jid_caps[from_jid.resource] = disco_tuple

            # nodes are the nodes subscribed with +notify
            nodes = tuple(self.hash_map[disco_tuple]['notify'])
            if not nodes:
                return
            # publishers are entities which have granted presence access to our user + user itself
            publishers = tuple(self.presence_map.get(from_jid_bare, ())) + (from_jid_bare,)

            # FIXME: add "presence" access_model (for node) for getLastItems
            last_items = yield self._backend.storage.getLastItems(publishers, nodes, ('open',), ('open',), True)
            # we send message with last item, as required by https://xmpp.org/extensions/xep-0163.html#notify-last
            for pep_jid, node, item, item_access_model in last_items:
                self.notifyPublish(pep_jid, node, [(from_jid, None, [item])])

    ## misc ##

    @defer.inlineCallbacks
    def getAutoSubscribers(self, recipient, nodeIdentifier, explicit_subscribers):
        """get automatic subscribers, i.e. subscribers with presence subscription and +notify for this node

        @param recipient(jid.JID): jid of the PEP owner of this node
        @param nodeIdentifier(unicode): node
        @param explicit_subscribers(set(jid.JID}: jids of people which have an explicit subscription
        @return (list[jid.JID]): full jid of automatically subscribed entities
        """
        auto_subscribers = []
        roster = yield self.getRoster(recipient)
        for roster_jid, roster_item in roster.iteritems():
            if roster_jid in explicit_subscribers:
                continue
            if roster_item.subscriptionFrom:
                try:
                    online_resources = self.caps_map[roster_jid]
                except KeyError:
                    continue
                for res, disco_tuple in online_resources.iteritems():
                     notify = self.hash_map[disco_tuple]['notify']
                     if nodeIdentifier in notify:
                         full_jid = jid.JID(tuple=(roster_jid.user, roster_jid.host, res))
                         auto_subscribers.append(full_jid)
        defer.returnValue(auto_subscribers)
