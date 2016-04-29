import cherrypy
import json
from pymongo import MongoClient

class Containers(object):
    def __init__(self):
        self.client = MongoClient()
        self.containers = self.client['WDTCS']['containers']

    def _getShipsLocations(self, contents):
        cherrypy.log('Retrieving ships'' locations.')

        matchStage = { '$match': { 'cargo': { '$in': contents.split(',') } } }
        groupStage = { '$group': {
                         '_id': '$shipName', 'location':{'$first':'$location.coordinates'},
                         'cargos':{'$addToSet': '$cargo'}, 'containers':{'$sum':1} } }
        sortStage = { '$sort': { '_id':1 } };

        pipeline = [ groupStage, sortStage ]
        if contents!='':
            pipeline.insert(0,matchStage)

        ships = list(self.containers.aggregate(pipeline))

        return json.dumps(ships)

    def _getTargets(self, lng, lat, radius, contents):
        cherrypy.log('Retrieving ships'' locations by target.')
        geoNearStage = { '$geoNear': {
                        'near': { 'type': 'Point', 'coordinates': [ lng, lat ] },
                        'distanceField': 'location',
                        'maxDistance': radius,
                        'limit': 1000000,
                        'includeLocs': 'location',
                        'spherical': 'true' } };
        if contents!='':
            geoNearStage['$geoNear']['query']={ 'cargo': { '$in' : contents.split(',') }}

        groupStage = { '$group': {
                         '_id': '$shipName', 'location':{'$first':'$location.coordinates'},
                         'cargos':{'$addToSet':'$cargo'},
                         'containers':{'$addToSet':'$container_id'} } };

        sortStage = { '$sort': { '_id':1 } };

        pipeline = [ geoNearStage, groupStage, sortStage ]

        ships = list(self.containers.aggregate(pipeline))

        return json.dumps(ships)

    def _parse_args(self, args):
        cherrypy.log('Arguments received:')
        cherrypy.log('  %s, %s, %s, %s' %
                     (args['lng'],args['lat'],args['radius'],args['contents']))

        return (float(args['lng']),float(args['lat']),int(args['radius']),args['contents'])

    @cherrypy.expose
    def index(self,**args):
        cherrypy.log('Containers WS is being invoked...')

        targets = []

        if 'lng' in args and 'lat' in args and 'radius' in args:
            lng, lat, radius, contents = self._parse_args(args)
            targets = self._getTargets(lng, lat, radius, contents)
        else:
            targets = self._getShipsLocations(args['contents'])

        return targets
         
