#!/usr/bin/env python

SERVER_NAME = 'doorbot server'
SERVER_VERSION = '20140415'

from __future__ import print_function

import os, sys, signal
import socket
import hashlib, hmac
import logging
import getopt

from server import BaseServer

def usage():
    print '{0} (v{1})'.format(SERVER_NAME, SERVER_VERSION)
    print 'Usage:'
    print '  {0} [-v|--verbose|-d|--debug]'.format(sys.argv[0])
    print ''
    print '  -f, --config    Configuration file path'
    print '  -v, --verbose   Verbose output'
    print '  -d, --debug     Very verbose output (DEBUG ONLY)'
    print '  -h, --help      Show this message.'
    print ''
    
if __name__ == '__main__':  
    # Default parameters
    config_path = None
    config = {
      'host' : 'localhost',
      'port' : 60405
    }

    # Get command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   'hvdf',
                                   ['help','verbose','debug','config'])
    except getopt.GetoptError, err:
        print(str(err), file=sys.stderr)
        usage()
        sys.exit(2)

    # Manage command line options
    for o, a in opts:
        if o in ('-v', '--verbose'):
            logging.basicConfig(level=logging.INFO)
        elif o in ('-d', '--debug'):
            logging.basicConfig(level=logging.NOTSET)
        elif o in ('-f', '--config'):
            config_path = a
        elif o in ('-h', '--help'):
            usage()
            sys.exit()
        else:
            assert False, 'Unhandled option: {0}'.format(o)

    # Load (and verify) server configuration
    if config_path is not None:
      with open(config,'r') as fd:
        config.update(json.load(fd))

    # Start the server
    logging.info('{0} (v{1}) running on {2}:{3}'.format(SERVER_NAME, SERVER_VERSION, config['host'], config['port']))
    
    s = BaseServer(server_config['host'],
                   server_config['port'],
                   server_config['handler'])

    s.serve_forever()