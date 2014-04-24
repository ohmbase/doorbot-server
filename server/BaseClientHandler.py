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
        self.message_uses_hmac = []
		
        # Register standard messages
        self.register_message_type('h', self.handle_hello, False)

    @classmethod
    def validate_options(cls, opts):
      ''' Validates optional **kwargs passed to the Handler. 
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
    
    def verify_hmac(self, message):
        """ Verifies a message's HMAC. Throws an InvalidRequest on a bad
            HMAC.
        """
        
        # Split up update request
        message_parts = message.split(' ')

		if len(message_parts) < 2:
		    raise InvalidRequest("No HMAC with message which requires it.")

        # Split message into HMAC and canonical string
        their_hmac = message_parts[-1]
        canonical_string = ' '.join(x for x in message_parts[:-1])

        # Check HMAC
        # .. against length
        if len(their_hmac) != 64:
            raise InvalidRequest("Malformed HMAC")
            
        # .. against HMAC computed here
        our_hmac = hmac.new(self.session['key'], canonical_string, hashlib.sha256).hexdigest()
        
        if our_hmac.lower() != their_hmac.lower():
            logging.debug("Could not verify HMAC:\n  ours:   {0}\n  theirs: {1}".format(our_hmac, their_hmac))
            raise InvalidRequest("Bad HMAC")
        
    def advance_session_key(self):
        """ Advances the session key (self.session['key']).
            Currently this is done by hashing the current session key
            with the client's master key.
        """
        self.session['key'] = hmac.new(self.session['profile']['key'], self.session['key'], hashlib.sha256).digest()

	def initialize_response_hmac(self, data = None):
        """ Initializes HMAC for response with the current session key
            (self.session['key']) using optionally supplied `data'.
        """
	    self.hmac = hmac.new(self.session['key'], data, hashlib.sha256)
	  
	def finalize_response(self, append_hmac = False):
        """ Send the end-of-message delimiter to the client.
            If `append_hmac' is true then the handler's HMAC (self.hmac)
            result is computed and sent followed by the end-of-message
            delimiter.
        """
      
        if append_hmac:
            # Send HMAC as last item folloed by end-of-message
	        self.socket.sendall(" {0}\n".format(self.hmac.hexdigest()))
            # Advance the session key
            self.advance_session_key()
	    else:
            # Send end-of-message
	        self.socket.sendall("\n")
		
		  
	def send(self, data, uses_hmac = False):
        """ Send `data' over `self.socket' (using sendall()).
            If `uses_hmac' is true then the handler's HMAC state for the
            message is updated with `data'.
        """
      
	    if uses_hmac:
	        self.hmac.update(data)
	  
	    self.socket.sendall(data)
        
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

		if len(client_id.strip('1234567890qwertyuiopasdfghjklzxcvbnm_')) > 0:
            raise InvalidRequest("Malformed client ID: {client_id}".format(client_id=client_id))
	    
        self.session['id'] = client_id

        # Load client profile
        self.session['profile'] = client.load_profile_for(client_id)
        self.session['profile']['key'] = self.__hmac(self.session['profile']['key']).digest()
        
        # Generate key material and key
        key_material = os.urandom(32)

        # Send key material for the session
        self.socket.send(key_material)
 
        logging.debug("key_material={0}".format([key_material]))
        logging.debug("master_key={0}".format([self.session['profile']['key']]))

        # Generate session key
        for i in range(self.key_gen_rounds):
	        key_material = hmac.new(self.session['profile']['key'], key_material, hashlib.sha256).digest()

        self.session['key'] = key_material # (sorry cryptographers)
        
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

        # Split message into the type and the data(/body)
        if ' ' in message:
          message_type, data = message.split(' ', 1)
        else:
          message_type = message
          data = ''
         
        # Authenticate message if required
        if message_type in self.message_uses_hmac:
            logging.debug("session_key={0}".format([self.session['key']]))
            # Verify HMAC
            self.verify_hmac(message)
            
            # Advance key
            self.advance_session_key()
            
            # Remove hmac from data
            data = data.rsplit(' ', 1)[0]
        
        logging.debug(self.session)
        logging.debug("Received message: {0} {1}".format(message_type, message_body))

        # Handle message type
        self.handlers[message_type](message_body)
