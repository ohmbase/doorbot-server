import os
import logging
import inspect
import json

from BaseHandler import BaseHandler

# No need to change unless you've
# extended the use of the profile.
DEFAULT_PROFILE = {
  'key':             None,
  'handler':       'BaseHandler',
  'handler_options': { 'path':   None,
                       'create': None,
                       'update': None }
}

def filename_for(client_id):
    '''Returns the profile filename for a given client_id
    '''
    return str(client_id) + '.json'

def validate(profile):
    '''Validates a profile.
    '''
    # Key
    if not profile['key']:
        raise ValueError("A pre-shared key (\"key\") is required.")

    # Validate handler options 
    profile['handler'].validate_options(profile['handler_options'])

def load_for(client_id):
    '''Loads a profile for a client_id located in config.PROFILE_DIR. 
    '''

    return load(os.path.join(config.PROFILE_DIR, filename_for(client_id)))

def load(profile_path):
    '''Loads a profile from disk based on filename.
    '''

    # Load the default profile
    profile = DEFAULT_PROFILE.copy() 

    # Update the default profile with the profile loaded from disk
    with open(profile_path, 'r') as f:
        profile.update(json.load(f))

    # Convert handler class name from string to a class
    if isinstance(profile['handler'], basestring):
        profile['handler'] = import_class(profile['type'])

    # Validate profile
    validate(profile)

    return profile

def import_class(full_name):
    '''Imports class from module given full path.
    '''
    module_name, class_name = full_name.rsplit('.', 1)
    return import_class(module_name, class_name)
    
def import_class(module_name, class_name):
    '''Imports class matching class_name from module matching module_name.
    '''
    # Import the module
    module = importlib.import_module(module_name)
    
    # Grab the class
    klass = getattr(module, class_name)

    # The class should be derived from BaseClientHandler
    if not inspect.isclass(klass) or not issubclass(klass, BaseClientHandler):
        raise TypeError('{0} is not a {1}-derived class.'.format(class_name, BaseClientHandler.__name__))

    return klass
