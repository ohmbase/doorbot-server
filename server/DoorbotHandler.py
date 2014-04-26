import logging
import os.path
import hashlib
import hmac
import json
from datetime import datetime

from BaseClientHandler import *
import user

# TODO Logging functionality
# TODO Database functionality

class DoorbotHandler(BaseHandler):
    ''' Handles Doorbot client communications.
          - authentication
          - logging of events
    '''    
    def __init__(self, sock, session, **options):
        BaseHandler.__init__(self, sock, session, **options)
        
        self.NOW_FORMAT  = '%Y-%m-%d %H:%M:%S' # Timestamp format
        self.DATE_FORMAT = '%Y%m%d'            # Date format
        
        # Unpack options
        # ... logging directory
        self.log_directory = options['log_directory']
        # ... user profiles directory
        self.users_directory = options['user_directory']
        
        # ... authenticator options (FUTURE)
        #self.authenticators
        #self.authentication_options = options['authentication'] # ... type : options
        
        # Register message types
        self.register_message_type('auth?', self.handle_authenticate, True)

    @classmethod
    def validate_options(cls, opts):
        # Validations for handler options

        if not opts['log_directory']:
            raise ValueError('client options: a log directory (\'log_directory\') is required.')
    
        if not opts['users_directory']:
            raise ValueError('client options: a users directory (\'users_directory\') is required.')
    
    def __log_path_for_now(self):
      return os.path.join(self.log_directory, '{date}.log'.format(date = datetime.now().strftime(self.DATE_FORMAT)))
    
    def __log(self, message):
      ''' Logs a message.
      '''
      with open(self.__log_path_for_now(), 'a') as f:
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
        # TODO generalize for authenticators -- self.authenticators[auth_type](auth_data)
        user_profile = user.find_by_auth_token(self.users_directory, auth_type, data)

        if user_profile is not None:
            send_authentication_response(True)
            self.__log('Authentication success ({type}, {user})'.format(type = auth_type, user = user_profile['name']))
        else:
            send_authentication_response(False)
            self.__log('Authentication failure ({type})'.format(type = auth_type))

    def send_authentication_response(self, success):
        self.initialize_response_hmac()
        if success:
          self.send('OK', True)
        else:
          self.send('NO', True)
        self.finalize_response(True)