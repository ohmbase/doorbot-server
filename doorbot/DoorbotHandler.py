import os, glob
import logging

from server.BaseClientHandler import *

class DoorbotHandler(BaseClientHandler):
    '''Performs user authentication and monitoring for a Doorbot.
    '''

    def __init__(self, sock, session, **options):
        BaseClientHandler.__init__(self, sock, session, **options)
        
        # Register authentication request message type
        self.register_message_type('auth?', self.handle_auth, False)
        
        # Unpack options
        self.users_directory = str(options['users_directory'])
        
    @classmethod
    def validate_options(cls, opts):
        # Validations for handler options
        required_keys = ['users_directory']
                         
        for k in required_keys:
          if not opts.has_key(k):
            raise ValueError('DoorbotHandler requires option \'{0}\' to be defined'.format(k))
        
    def handle_auth(self, data):
        '''Parses authentication request.
        '''
        logging.debug('Handling auth?: {0}'.format(data))

        # Unpack arguments
        type, auth_info = data.split(' ', 1)
        
        # Authenticate
        if authenticate(type, auth_info):
          self.sock.send('OK\n') # authentication success
        else:
          self.sock.send('NO\n') # authentication failure
          
    def authenticate(type, auth_info):
        # FUTURE authentication by type
    
        # TODO data interface into Users
            
        return True