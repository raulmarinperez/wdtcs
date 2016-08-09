import cherrypy
import os, os.path
import argparse

class WDTCS(object):

    def __init__(self, WDTCS_HOME):
        self._WDTCS_HOME = WDTCS_HOME

    @cherrypy.expose
    def index(self):
        cherrypy.log('Requesting the main page...')
        return open('%s/www/index.htm' % self._WDTCS_HOME)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WDTCS Web Server')
    parser.add_argument('WDTCS_HOME', help="Home folder where the main files are located")

    # process the command line arguments
    args = parser.parse_args()

    print ("WDTCS_HOME: %s" % args.WDTCS_HOME)
    # start the web server
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
    conf = { '/': { 'tools.sessions.on': True,
                    'tools.response_headers.on': True,
                    'tools.staticdir.root': '%s/www' % args.WDTCS_HOME },
             '/js': { 'tools.staticdir.on': True,
                      'tools.staticdir.dir': './js' },
             '/css': { 'tools.staticdir.on': True,
                       'tools.staticdir.dir': './css' },
             '/img': { 'tools.staticdir.on': True,
                       'tools.staticdir.dir': './img' }
           }
    cherrypy.quickstart(WDTCS(args.WDTCS_HOME), '/', conf)
