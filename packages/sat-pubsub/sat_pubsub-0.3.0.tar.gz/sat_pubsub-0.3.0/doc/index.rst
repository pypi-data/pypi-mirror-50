.. SàT PubSub documentation master file, created by
   sphinx-quickstart on Wed Jul 24 08:06:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SàT PubSub documentation
========================

SàT PubSub is a XMPP PubSub service component (XEP-0060) It's based on Ralph Meijer's
Idavoll, and provides special features necessary for the « Salut à Toi » project
(https://salut-a-toi.org) , but it can also be used for any other XMPP project.  The use
of a standard external component allow to use this features with most XMPP servers.  One
of the main addition is fine access tuning for PubSub, which allow the publication of
items for only some groups, even if the entire node is open. The protocol is explained on
http://www.goffi.org/post/2012/06/24/Fine-access-tuning-for-PubSub for the moment, and a
protoxep should be proposed to the XSF in the future…


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   installation.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
