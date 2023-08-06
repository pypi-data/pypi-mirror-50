#!/usr/bin/python
#-*- coding: utf-8 -*-

# Copyright (c) 2012-2019 Jérôme Poisson
# Copyright (c) 2003-2011 Ralph Meijer


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
# --

# This program is based on Idavoll (http://idavoll.ik.nu/),
# originaly written by Ralph Meijer (http://ralphm.net/blog/)
# It is sublicensed under AGPL v3 (or any later version) as allowed by the original
# license.

# --

# Here is a copy of the original license:

# Copyright (c) 2003-2011 Ralph Meijer

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import csv
import sat_pubsub
import sys
from twisted.application.service import IServiceMaker
from twisted.application import service
from twisted.python import usage, log
from twisted.words.protocols.jabber.jid import JID
from twisted.plugin import IPlugin

from wokkel.component import Component
from wokkel.disco import DiscoHandler
from wokkel.generic import FallbackHandler, VersionHandler
from wokkel.iwokkel import IPubSubResource
from wokkel import data_form
from wokkel import pubsub
from wokkel import rsm
from wokkel import mam
from zope.interface import implements

from sat_pubsub import const
from sat_pubsub import mam as pubsub_mam
from sat_pubsub import pubsub_admin
from sat_pubsub.backend import BackendService, ExtraDiscoHandler
from sat_pubsub.schema import SchemaHandler
from sat_pubsub.privilege import PrivilegesHandler
from sat_pubsub.delegation import DelegationsHandler
from os.path import expanduser, realpath
import ConfigParser


def coerceListType(value):
    return csv.reader(
        [value], delimiter=",", quotechar='"', skipinitialspace=True
    ).next()


def coerceJidListType(value):
    values = [JID(v) for v in coerceListType(value)]
    if any((j.resource for j in values)):
        raise ValueError(u"you must use bare jids")
    return values



OPT_PARAMETERS_BOTH = [
    ['jid', None, None, 'JID this component will be available at'],
    ['xmpp_pwd', None, None, 'XMPP server component password'],
    ['rhost', None, '127.0.0.1', 'XMPP server host'],
    ['rport', None, '5347', 'XMPP server port'],
    ['backend', None, 'pgsql', 'Choice of storage backend'],
    ['db_user', None, None, 'Database user (pgsql backend)'],
    ['db_name', None, 'pubsub', 'Database name (pgsql backend)'],
    ['db_pass', None, None, 'Database password (pgsql backend)'],
    ['db_host', None, None, 'Database host (pgsql backend)'],
    ['db_port', None, None, 'Database port (pgsql backend)'],
    ]
# here for future use
OPT_PARAMETERS_CFG = [
    ["admins_jids_list", None, [], "List of administrators' bare jids",
     coerceJidListType]
    ]

CONFIG_FILENAME = u'sat'
# List of the configuration filenames sorted by ascending priority
CONFIG_FILES = [realpath(expanduser(path) + CONFIG_FILENAME + '.conf') for path in (
    '/etc/', '/etc/{}/'.format(CONFIG_FILENAME),
    '~/', '~/.',
    '.config/', '.config/.',
    '', '.')]
CONFIG_SECTION = 'pubsub'


class Options(usage.Options):
    optParameters = OPT_PARAMETERS_BOTH

    optFlags = [
        ('verbose', 'v', 'Show traffic'),
        ('hide-nodes', None, 'Hide all nodes for disco')
    ]

    def __init__(self):
        """Read SàT Pubsub configuration file in order to overwrite the hard-coded default values.

        Priority for the usage of the values is (from lowest to highest):
            - hard-coded default values
            - values from SàT configuration files
            - values passed on the command line
        """
        # If we do it the reading later: after the command line options have been parsed, there's no good way to know
        # if the  options values are the hard-coded ones or if they have been passed on the command line.

        # FIXME: must be refactored + code can be factorised with backend
        config_parser = ConfigParser.SafeConfigParser()
        config_parser.read(CONFIG_FILES)
        for param in self.optParameters + OPT_PARAMETERS_CFG:
            name = param[0]
            try:
                value = config_parser.get(CONFIG_SECTION, name)
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                try:
                    param[2] = param[4](value)
                except IndexError: # the coerce method is optional
                    param[2] = value
                except Exception as e:
                    log.err(u'Invalid value for setting "{name}": {msg}'.format(
                        name=name, msg=e))
                    sys.exit(1)
            except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
                pass
        usage.Options.__init__(self)
        for opt_data in OPT_PARAMETERS_CFG:
            self[opt_data[0]] = opt_data[2]

    def postOptions(self):
        if self['backend'] not in ['pgsql', 'memory']:
            raise usage.UsageError("Unknown backend!")
        if self['backend'] == 'memory':
            raise NotImplementedError('memory backend is not available at the moment')

        self['jid'] = JID(self['jid']) if self['jid'] else None


class SatPubsubMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "sat-pubsub"
    description = u"Salut à Toi Publish-Subscribe Service Component".encode('utf-8')
    options = Options

    def makeService(self, config):
        if not config['jid'] or not config['xmpp_pwd']:
            raise usage.UsageError("You must specify jid and xmpp_pwd")
        s = service.MultiService()

        # Create backend service with storage

        if config['backend'] == 'pgsql':
            from twisted.enterprise import adbapi
            from sat_pubsub.pgsql_storage import Storage
            from psycopg2.extras import NamedTupleConnection
            keys_map = {
                'db_user': 'user',
                'db_pass': 'password',
                'db_name': 'database',
                'db_host': 'host',
                'db_port': 'port',
            }
            kwargs = {}
            for config_k, k in keys_map.iteritems():
                v = config.get(config_k)
                if v is None:
                    continue
                kwargs[k] = v
            dbpool = adbapi.ConnectionPool('psycopg2',
                                           cp_reconnect=True,
                                           client_encoding='utf-8',
                                           connection_factory=NamedTupleConnection,
                                           **kwargs
                                           )
            st = Storage(dbpool)
        elif config['backend'] == 'memory':
            raise NotImplementedError('memory backend is not available at the moment')

        bs = BackendService(st, config)
        bs.setName('backend')
        bs.setServiceParent(s)

        # Set up XMPP server-side component with publish-subscribe capabilities

        cs = Component(config["rhost"], int(config["rport"]),
                       config["jid"].full(), config["xmpp_pwd"])
        cs.setName('component')
        cs.setServiceParent(s)

        cs.factory.maxDelay = 900

        if config["verbose"]:
            cs.logTraffic = True

        FallbackHandler().setHandlerParent(cs)
        VersionHandler(u'SàT Pubsub', sat_pubsub.__version__).setHandlerParent(cs)
        DiscoHandler().setHandlerParent(cs)

        ph = PrivilegesHandler(config['jid'])
        ph.setHandlerParent(cs)
        bs.privilege = ph

        resource = IPubSubResource(bs)
        resource.hideNodes = config["hide-nodes"]
        resource.serviceJID = config["jid"]

        ps = (rsm if const.FLAG_ENABLE_RSM else pubsub).PubSubService(resource)
        ps.setHandlerParent(cs)
        resource.pubsubService = ps

        if const.FLAG_ENABLE_MAM:
            mam_resource = pubsub_mam.MAMResource(bs)
            mam_s = mam.MAMService(mam_resource)
            mam_s.addFilter(data_form.Field(var=const.MAM_FILTER_CATEGORY))
            mam_s.setHandlerParent(cs)

        pa = pubsub_admin.PubsubAdminHandler(bs)
        pa.setHandlerParent(cs)

        sh = SchemaHandler()
        sh.setHandlerParent(cs)

        # wokkel.pubsub doesn't handle non pubsub# disco
        # and we need to announce other feature, so this is a workaround
        # to add them
        # FIXME: propose a patch upstream to fix this situation
        ed = ExtraDiscoHandler()
        ed.setHandlerParent(cs)

        # XXX: delegation must be instancied at the end,
        #      because it does some MonkeyPatching on handlers
        dh = DelegationsHandler()
        dh.setHandlerParent(cs)
        bs.delegation = dh

        return s

serviceMaker = SatPubsubMaker()
