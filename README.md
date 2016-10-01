freifunkh kundenservice
=======================

This is a simple bot hanging around in #freifunkh channel in the
hackint irc network. Be aware that this is hacked quick and dirty.

Installation
------------

- Install [sopel](https://sopel.chat/) from your favorite package manager.

- Clone this repository as ~/.sopel/modules:

        $ mkdir ~/.sopel/
        $ git clone https://github.com/freifunkh/kundenservice ~/.sopel/modules

- Use this configuration as testing configuration:

        # ~/.sopel/default.cfg
        [core]
        nick = Kundenservice-testing
        host = irc.hackint.org
        use_ssl = true
        verify_ssl = false
        port = 9999
        channels = #freifunkh-test
        enabled = forum
        owner = <your-irc-name>

        [freifunkh]
        channel = #freifunkh-test
        forum_rss_url = http://hannover.freifunk.net/forum/syndication.php?limit=15

- Start sopel:

        $ sopel

Features
--------

- Notifies about new threads in https://hannover.freifunk.net/forum

Hacking References
------------------

- We introduced the ```freifunkh.channel``` config option to specify the
  channel, where the modules of this repository write in. So it is possible
  to activate some foreign modules, which can use other channels.
- [sopel plugin documentation](https://sopel.chat/docs/plugin.html)
