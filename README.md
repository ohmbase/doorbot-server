# _doorbot_ server

## Overview

_doorbot_ is an access control system designed to control and report on access to shared spaces.

## Usage



## Server configuration

`TODO`

### Example `config.json`

`TODO`

## Client profiles

`TODO`

### Example client profile

    {
      "key" : "secret123",
      "type" : "server.DoorbotHandler.DoorbotHandler",
      "options" : {
        "users_directory" : "/path/to/users",
        "logging_directory" : "/path/to/log"
      }
    }

Note: client ID is derived from the file name (e.g. `doorbot_frontdoor.json` is for client with ID `doorbot_frontdoor`)

## User profiles

`TODO`

### Example user profile

    {
      "name" : "Chris R.",
      "rfid" : "0123456789",
      "prepay" : {
        "balance" : 0,
        "timeout" : "20140101000000"
      }
    }

Note: file name is only meaningful to human administrators.

`TODO - different fields`

## Extending _doorbot_ server

Client configurations can specify the type of handler object they wish to use. _doorbot_ clients want to use a handler which provides _doorbot_-specific functionality. However, handlers can be written to extend the capabilities of the server. Custom client handlers should inherit `BaseClientHandler` to include client bootstrapping functionality (i.e. the 'hello' message). See `server/DoorbotHandler.py` for an example of extending `BaseClientHandler`.

## See also

* [doorbot-client](https://github.com/ohmbase/doorbot-server) - _doorbot_ client (Arduino)
* [doorbot-board](https://github.com/ohmbase/doorbot-board) - _doorbot_ hardware

## doorbot-server License

    Copyright (c) 2011-2014, Ohm Base Hackerspace
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
        * Redistributions of source code must retain the above
          copyright notice, this list of conditions and the following
          disclaimer.
        * Redistributions in binary form must reproduce the above
          copyright notice, this list of conditions and the following
          disclaimer in the documentation and/or other materials
          provided with the distribution.
        * Neither the name of the Ohm Base Hackerspace nor the names of
          its contributors may be used to endorse or promote products
          derived from this software without specific prior written
          permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL OHM BASE
    HACKERSPACE BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
    USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.