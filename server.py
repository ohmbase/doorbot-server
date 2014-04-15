#!/usr/bin/env python

import os, sys, signal
import socket
import hashlib, hmac
import logging
import getopt
#import rrdtool

import doorbot
from doorbot.BaseServer import BaseServer

def usage():
    print "doorbot server" 
    print "Usage:"
    print "   Running the server:"
    print "       {0} [-v|--verbose|-d|--debug]".format(sys.argv[0])
    print ""
    print "  -v, --verbose   Verbose output"
    print "  -d, --debug     Very verbose output (DEBUG ONLY)"
    print "  -h, --help      Show this message."
    print ""
    print "See doorbot/config.py for server configuration."
    
if __name__ == "__main__":  

    # Get command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hvd",
                                   ["help","verbose","debug"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    # Manage command line options
    for o, a in opts:
        if o in ('-v', '--verbose'):
            logging.basicConfig(level=logging.INFO)
        elif o in ('-d', '--debug'):
            logging.basicConfig(level=logging.NOTSET)
        elif o in ('-h', '--help'):
            usage()
            sys.exit()

        # Server settings
        #elif o in ('-h', '--host'):
        #    doorbot.config.HOST = a
        #elif o in ('-p', '--port'):
        #    doorbot.config.PORT = a
        #elif o in ('--profile-dir'):
        #    doorbot.config.PROFLIE_DIR = a
        #elif o in ('--rrds'):
        #    doorbot.config.RRD_DIR = a
        else:
            assert False, "Unhandled option: {0}".format(o) 

    # Make sure our directories exist
    if not os.path.exists(doorbot.config.PROFILE_DIR):
        os.makedirs(doorbot.config.PROFILE_DIR)

    # Start the server
    logging.info("RRDuino server running on {0}:{1}".format(doorbot.config.HOST, doorbot.config.PORT))
    server = BaseServer(doorbot.config.HOST,
                        int(doorbot.config.PORT),
                        doorbot.config.DEFAULT_HANDLER)

    server.serve_forever()
