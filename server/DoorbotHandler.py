import logging
import os.path
import hashlib
import hmac
import json
from datetime import datetime

from BaseClientHandler import *

# TODO Logging functionality
# TODO Database functionality

class DoorbotHandler(BaseHandler):
    '''Uses a flat-file log for the connected client.
    '''
    
    def __init__(self, sock, session, **options):
        BaseHandler.__init__(self, sock, session, **options)
        
        self.NOW_FORMAT  = '%Y-%m-%d %H:%M:%S' # Timestamp format
        self.DATE_FORMAT = '%Y%m%d'            # Date format
        self. authenticators = {
          'rfid' : __authenticate_rfid
        }
        
        # Unpack options
        # ... logging options
        self.log_directory = options['logging']
        
        # ... authenticator options
        self.authentication_options = options['authentication'] # ... type : options
        
        # Register message types
        self.register_message_type('auth?', self.handle_authenticate, True)
        self.register_message_type('cache?', self.handle_check_auth_cache, True)

    @classmethod
    def validate_options(cls, opts):
        # Validations for handler options

        if not opts['log_path']:
            raise ValueError('\'handler_options\': a file path (\'log_path\') is required.')
    
        if not opts['rfid_path']:
            raise ValueError('\'handler_options\': a file path (\'rfid_path\') is required.')
    
    def __authenticate_rfid(self, data):
        ''' Authenticates an RFID token for this client.
            TODO put in own class/module?
        '''
    
    def _log_it(self, message):
      ''' Logs a message.
      '''
      with open(self._log_path_for_now(), 'a') as f:
        f.write('[{timestamp}] {message}\n'.format(timestamp = datetime.now().strftime(self.NOW_FORMAT),
                                                   message = message))
      
    def handle_authenticate(self, message_data):
        ''' Handles an authentication message (auth?). This message is
            intended for testing authentication credentials for access
            control. These events will be logged.
            
            Message format (general): auth? <method> <method-specific data> <hmac>
            Message format (RFID): auth? rfid <token hash> <hmac>
            Message format (PIN): auth? pin <pin hash> <hmac>
        '''
        
        # Split message data
        parts = message_data.split(' ', 1)
        
        if len(parts) != 2:
          raise InvalidRequest('Malformed auth? request.')
        
        auth_type, auth_data = parts[0], parts[1]
        
        # Test authentication
        if self.authenticators.has_key(auth_type):
          if self.authenticators[auth_type](auth_data):
            on_authentication_success(auth_type, auth_data)
          else:
            on_authentication_failure(auth_type, auth_data)
        else:
          on_authentication_failure(auth_type, auth_data)
        
    def handle_check_auth_cache(self):
        ''' Handles a cache-check message (cache?). This message allows
            the client to test its cache for out-of-date/stale entries.
            
            TODO - age? db state token? full ask?
        '''
        pass

    def on_authentication_success(self, auth_type, auth_data):
        self.initialize_response_hmac()
        self.send('OKAY', True)
        self.finalize_response(True)
        
        self.log('')
        
    def on_authentication_failure(self, auth_type, auth_data):
        self.initialize_response_hmac()
        self.send('FAIL', True)
        self.finalize_response(True)
        
        self.log('')