doorbot server
==============

`TODO`

Usage
-----

`TODO`

Server configuration
--------------------

`TODO`

Client configuration
--------------------

`TODO`

User profiles
-------------

`TODO`

Uses beyond doorbot
-------------------

Client configurations can specify the type of handler object they wish to use. doorbot clients would want use the handler which provides doorbot-specific functionality, however, handlers can be written to extend the capabilities of the server (e.g. event logging). Custom client handlers should inherit `server.BaseClientHandler` to include client bootstrapping functionality (i.e. 'hello' messages) which allows client configurations to be loaded and the new handler instantiated. See `doorbot/DoorbotHandler.py` for an example of extending `server.BaseClientHander`.