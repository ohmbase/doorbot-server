import os
import socket
import logging
import hashlib, hmac

import profile

class InvalidRequest(Exception):
    pass

class BaseClientHandler:
    """ Base class of all client handlers.
        This class implements the 'hello' handler as well as providing the foundation for general message verification.
        Subclasses can register their own handling functions in __init__ using register_message_type.
    """
    
    # "Default buffer sizes for rfile, wfile.
    # We default rfile to buffered because otherwise it could be
    # really slow for large data (a getc() call per byte); we make
    # wfile unbuffered because (a) often after a write() we want to
    # read and we need to flush the line; (b) big writes to unbuffered
    # files are typically optimized by stdio even when big reads
    # aren't."
    #
    # -- Source: http://svn.python.org/projects/python/trunk/Lib/SocketServer.py
    rbufsize = -1
    wbufsize = 0

    def __init__(self, sock, session, **options):
        self.session = session
        self.socket = sock
        self.rfile_up()
        self.handlers = {}
        
        # Register standard messages
        self.register_message_type('h', self.handle_hello)

    @classmethod
    def validate_options(cls, opts):
      ''' Validates optional **kwargs passed to handler. 
          Should be implemented by derived classes.
          If a derived class wants to pass validations to its base class
          then it should use super() or similar.
      '''
      pass

    def register_message_type(self, message_type, callback):
        """ Registers a handler function for messages beginning with
            'message_type'. Handler functions should accept a single
            parameter (e.g 'data') which is the received message with the
            'message_type' and HMAC removed. If the message type requires
            authentication, the parameter 'requires_hmac' should be set to True.
        """
        
        # Register the handler
        self.handlers.update({message_type: callback})
        
        # FUTURE require message authentication
        
    def readline(self):
        return self.rfile.readline()

    def rfile_up(self):
        self.rfile = self.socket.makefile('rb', self.rbufsize)

    #def wfile_up(self):
    #    self.wfile = self.socket.makefile('wb', self.wbufsize)

    #def wfile_down(self):
    #    if not self.wfile.closed:
    #        self.wfile.flush()
    #    self.wfile.close()

    def handle_hello(self, data):
        """ Handles the 'hello' message.
            Format: 'hello <client_id>\n'
        """
        logging.debug('Handling hello: {0}'.format(data))

        # Read client ID
        client_id = data.strip()

        if len(client_id) == 0:
            logging.debug("Empty client ID")
            raise InvalidRequest("Empty client ID")

        self.session['id'] = client_id

        # Load client profile
        self.session['profile'] = client.load_profile_for(client_id)
        self.session['profile']['key'] = self.__hmac(self.session['profile']['key']).digest()
        
        # FUTURE handshake/authentication
        
        self.socket.send('Hello, {0}\n'.format(client_id))

    def handle(self):
        """ Determines the message content and delivers the message to the
            appropriate (registered) handler function for further processing.
            
            #If the message type requires HMAC authentication, then the message
            #is automagically verified. If the message is not authenticated,
            #an error will be raised. See verify_hmac() for details.
        """
        # Get message
        message = self.readline().rstrip()

        logging.debug("({0}) '{1}'".format(len(message), message))

        if not message:
            raise socket.error("Client disconnected")

        # Split message into the type and the body
        message_type, message_body = message.split(' ', 1)
         
        # FUTURE authenticate message
        
        logging.debug(self.session)
        logging.debug("Received message: {0} {1}".format(message_type, message_body))

        # Handle message type
        self.handlers[message_type](message_body)
