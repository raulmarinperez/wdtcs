import cherrypy
import os, os.path
import lib.api

class WRYD(object):
    def __init__(self):
        self.containers = lib.api.Containers()

    def _cp_dispatch(self, vpath):
        strpath = '/'.join(vpath)
        cherrypy.log('vpath: ' + strpath)
        if strpath.startswith('containers'):
            cherrypy.log('Returning the API instance')
            vpath.pop(0)
            return self.containers

        return vpath

    @cherrypy.expose
    def index(self):
        cherrypy.log('Requesting the main page...')
        return open('web/index.htm')

if __name__ == '__main__':
    cherrypy.config.update( {'server.socket_host': '0.0.0.0'} )
    conf = { '/': { 'tools.sessions.on': True,
                    'tools.response_headers.on': True,
                    'tools.staticdir.root': os.path.abspath(os.getcwd())+'/web' },
             '/img': { 'tools.staticdir.on': True,
                       'tools.staticdir.dir': './img' }
           }
    cherrypy.quickstart(WRYD(), '/', conf)
