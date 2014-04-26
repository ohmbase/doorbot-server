import os
import logging
import inspect
import json

from BaseHandler import BaseHandler

# TODO perhaps allow register callbacks for before/after load, before/after save, validate

def filename_for(user_id):
    '''Returns the profile filename for a given user_id
    '''
    return str(user_id) + '.json'

def validate(profile):
    '''Validates a user profile.
    '''
    
    # TODO name, authentication
    
    # Name
    if not profile.has_key('name'):
        raise ValueError('User requires a name ("name").')

def load_for(user_id):
    '''Loads a profile for a user_id located in config.PROFILE_DIR. 
    '''
    return load(os.path.join(config.PROFILE_DIR, filename_for(user_id)))

def load(profile_path):
    '''Loads a profile from disk based on filename.
    '''
    # Load the default profile
    profile = {} 

    # Update the default profile with the profile loaded from disk
    with open(profile_path, 'r') as f:
        profile.update(json.load(f))

    # Validate profile
    validate(profile)

    # Remember where it was loaded from
    profile['_path'] = profile_path
    
    # Check raw RFID tokens
    # TODO authenticator modules clean own sections
    try: 
      RFID_LENGTH = 10
      user_token = profile['authentication']['rfid']['token']
      if len(user_token) == RFID_LENGTH:
        user_token = hashlib.sha256(user_token).hexdigest()
        save(profile)
    except KeyError as e:
      # Likely profile['authentication']['rfid']['token'] not defined... that's OK
      pass
      
    return profile
    
def save(profile, profile_path=None):
    # Strip out _path if added
    if profile.has_key('_path'):
      if profile_path is None:
        profile_path = profile['_path']
      del profile['_path']
    
    # TODO anything that needs to be modified before save?
    
    with open(profile_path, 'w') as f:
      json.save(profile, f)

    # Add _path back to profile
    return profile['_path'] = profile_path

def test_rfid_token(profile, token):
    
    # If the token is a raw RFID token (e.g. 10 characters long)
    # then we want to hash it and save it back out
    user_token = profile['authentication']['rfid']['token']
    if len(user_token) == RFID_LENGTH:
      user_token = hashlib.sha256(user_token).hexdigest()
      save(profile)
      
    return (user_token.lower() == token.lower())
        
def find_by_auth_token(users_directory, auth_type, auth_token):
    # TODO move authenticators into their own modules/classes, register typical functions
    #      e.g. test rfid
    token_tests = {
      'rfid' : test_rfid_token
    }

    # List all profiles in user profiles directory
    user_profiles = glob.glob(os.path.join(self.users_directory, '*.json')
    
    # Test each user profile for tokens
    for user_path in user_profiles:
      user_profile = load(user_path)
        
      try:
        # Test token against user profile's token
        if token_tests[auth_type](user_profile, auth_token):
          return user_profile
      except KeyError, TypeError as e:
        # Profile does not contain authentication information (ignore -- doesn't match)
        # TODO invalid permissions denied on save-out?
        pass
        
    return None