============
Installation
============

This are the instructions to install SàT Pubsub.

Please note that SàT PubSub, as all SàT ecosystem, is still using Python 2 (this will
change for SàT PubSub 0.4 version which will be Python 3 only), so all instructions below
have to be made using python 2.

.. note::

   SàT PubSub is not released yet and this documentation is work in progress


Requirements
------------

- Python 2.7.x
- Twisted >= 15.2.0:
   - Twisted Core
   - Twisted Words
- Wokkel >= 0.7.1 (http://wokkel.ik.nu/)
- A XMPP server that supports the component protocol (XEP-0114),
  and, to enable the micro-blogging feature, Namespace Delegation (XEP-0355)
  and privileged entity (XEP-0356) are needed.
  We recommend using Prosody with mod_privilege and mod_delegation modules (those modules
  are maintained by us).
- SàT tmp (http://repos.goffi.org/sat_tmp) is currently needed for MAM and RSM handling

For the PostgreSQL backend, the following is also required:

- PostgreSQL >= 9.5 (including development files for psycopg2)
- psycopg2

Installation From Sources
-------------------------

To install SàT PubSub we'll work in a virtual environment. On Debian and derivatives you
should easily install dependencies with this::

    sudo apt-get install postgresql python-dev mercurial virtualenv

Now go in a location where you can install SàT Pubsub, for instance your home directory::

    $ cd

And enter the following commands (note that *virtualenv2* may be named
*virtualenv* on some distributions, just be sure it's Python **2** version)::

    $ virtualenv2 env
    $ source env/bin/activate
    $ pip install hg+https://repos.goffi.org/sat_pubsub

Post Installation
-----------------

Once SàT Pubsub is installed, you'll need to create a PostgreSQL user, and create the
database::

    % sudo -u postgres createuser -d -P $(whoami)
    % createdb pubsub
    % cd /tmp && wget https://repos.goffi.org/sat_pubsub/raw-file/tip/db/pubsub.sql
    % psql pubsub < pubsub.sql


.. _prosody_configuration:

Prosody Configuration
---------------------

SàT PubSub can work with any XMPP server (which supports components), but if you want to
use it as your PEP service, you need a server which supports `XEP-0355`_ and `XEP-0356`_.

Below you'll find the instruction to use SàT PubSub as a PEP service with Prosody:

-  add these two lines at the end of your ``prosody.cfg.lua`` file, adapting them to your XMPP
   server domain (virtual host) and selecting a password of your choice:

.. sourcecode:: lua

    Component "sat-pubsub.<xmpp_domain>"
            component_secret = "<password>"

-  there are extra steps to enable the micro-blogging feature with Prosody. Please follow
   the installation and configuration instructions that are given on these pages:

   - https://modules.prosody.im/mod_delegation.html
   - https://modules.prosody.im/mod_privilege.html

To keep your modules up to date, we recommend to clone the full modules
repository and then to symlink them like that:

.. sourcecode:: shell

    % cd /path/to/install_dir
    % hg clone https://hg.prosody.im/prosody-modules
    % cd /path/to/prosody_plugins
    % ln -sf /path/to/install_dir/prosody-modules/mod_delegation ./
    % ln -sf /path/to/install_dir/prosody-modules/mod_privilege ./

Or course, you have to adapt ``/path/to/install_dir`` to the directory where you want to
install the modules, and ``/path/to/prosody_plugins`` to the directory where prosody
modules are installed (hint: check ``prosodyctl about`` to find the latter). The ``ln``
commands may have to be run as root depending on your installation.

Once your symlinks are set, to update the modules we just need to type this:

.. sourcecode:: shell

    % cd /path/to/install_dir/prosody-modules
    % hg pull -u

Here is an example of how your ``prosody.cfg.lua`` should look like with
``mod_delegation`` and ``mod_privilege`` activated:

.. sourcecode:: lua

    [...]
    modules_enabled = {
                  [...]
                  "delegation";
                  "privilege";
    }
    [...]
    VirtualHost "<xmpp_domain>"
      privileged_entities = {
        ["sat-pubsub.<xmpp_domain>"] = {
          roster = "get";
          message = "outgoing";
          presence = "roster";
        },
      }
      delegations = {
          ["urn:xmpp:mam:2"] = {
            filtering = {"node"};
            jid = "sat-pubsub.<xmpp_domain>";
          },
          ["http://jabber.org/protocol/pubsub"] = {
            jid = "sat-pubsub.<xmpp_domain>";
          },
          ["http://jabber.org/protocol/pubsub#owner"] = {
            jid = "sat-pubsub.<xmpp_domain>";
          },
          ["https://salut-a-toi/protocol/schema:0"] = {
            jid = "sat-pubsub.<xmpp_domain>";
          },
          ["http://jabber.org/protocol/disco#items:*"] = {
            jid = "sat-pubsub.<xmpp_domain>";
          },
          ["https://salut-a-toi.org/spec/pubsub_admin:0"] = {
            jid = "sat-pubsub.<xmpp_domain>";
          },
      }

    Component "sat-pubsub.<xmpp_domain>"
       component_secret = "<password>"
       modules_enabled = {"delegation", "privilege"}

Of course, you still have to replace and adapt to your own settings.

.. _XEP-0355: https://xmpp.org/extensions/xep-0355.html
.. _XEP-0356: https://xmpp.org/extensions/xep-0356.html

Running SàT PubSub
------------------

The minimal example for running sat_pubsub is:

  % twistd sat_pubsub

This will start the service and run it in the background. It generates a
file twistd.pid that holds the PID of the service and a log file twistd.log.
The twistd utility has a fair number of options that might be useful, and
can be viewed with:

  % twistd --help

When the service starts, it will connect to the XMPP server at the local machine using the
component protocol, and assumes the JID ``pubsub``. This assumes a couple of defaults
which can be overridden by passing parameters to the twistd plugin. You can get an
overview of the parameters and their defaults using:

  % twistd sat_pubsub --help

In particular, the following parameters will be of interest:

 ``--jid``
    The Jabber ID the component will assume.

 ``--rport``
    the port number of the XMPP server to connect to

 ``--xmpp_pwd``
    the secret used to authenticate with the XMPP server.

For example::

  twistd sat_pubsub --jid=sat-pubsub.<your_xmpp_domain> --xmpp_pwd=<password>

You can set your options in ``sat.conf`` which is the same file used as for Salut à Toi
ecosystem. Please check backend ``configuration`` section for details. The SàT PubSub
options must be in ``[pubsub]`` section.

