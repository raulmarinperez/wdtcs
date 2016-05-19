import cherrypy
import json
from pymongo import MongoClient

class Containers(object):
    def __init__(self):
        self.client = MongoClient()
        self.ships = self.client['WDTCS']['ships']
        self.containers = self.client['WDTCS']['containers']
        self.oceans = self.client['WDTCS']['oceans']

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

    def _getSeaGeometry(self, sea):
        sea_dict = { 'Biscay': 'Bay of Biscay',
                     'Medi': 'Mediterranean Sea',
                     'North': 'NORTH ATLANTIC OCEAN',
                     'Caribbean': 'Caribbean  Sea' }
        return self.oceans.find_one({'name':sea_dict[sea]})['geometry']

    def _getGeoWithin(self, bb_ne, bb_sw, sea):
        if sea=='':
            return {'$box' : [bb_sw,bb_ne]}

        return {'$geometry' : self._getSeaGeometry(sea) }

    def _getTargetsBB(self, bb_ne, bb_sw, contents, sea):
        cherrypy.log('Retrieving ships'' locations by bounding box and contents.')

        #matchStage = {'$match' :{'location' : {'$geoWithin' : {'$box' : [bb_sw,bb_ne]}}}}
        matchStage = {'$match' :{'location' : {'$geoWithin' : self._getGeoWithin(bb_ne, bb_sw, sea)}}}
        lookup = {'$lookup' : {'from': "containers", 'as': "cargo", 'localField': "Name", 'foreignField': "shipName"}}
        unwind = {'$unwind': "$cargo"}
        matchStage2 = {'$match' : {'cargo.cargo' : { '$in' : contents.split(',') } } }
        cherrypy.log('matchStage2: ' + contents)
        group = {'$group' : {'_id': {'ship': "$Name", 'cargo' : "$cargo.cargo", 'route': "$route", 'location': "$location"}, 'sum': {'$sum': "$cargo.Tons"}}}
        project = {'$project': {'_id' : {'ship': "$_id.ship", 'route': "$_id.route", 'location': "$_id.location"}, 'cargo' : {'type' : "$_id.cargo", 'Tons': "$sum"}}}
        group2 = {'$group' : {'_id': "$_id", 'cargo': {'$push': "$cargo"}}}

        if contents!='':
            pipeline = [ matchStage, lookup, unwind, matchStage2, group, project, group2 ]
        else:
            pipeline = [ matchStage, lookup, unwind, group, project, group2 ]

        ships = list(self.ships.aggregate(pipeline))

        cherrypy.log('Ships numbers: ' + str(len(ships)))
        return json.dumps(ships)

    def _parse_boundingbox_args(self, args):
        cherrypy.log('Arguments received:')
        cherrypy.log('  %s, %s, %s, %s' %
                     (args['bb_ne'],args['bb_sw'],args['contents'],args['sea']))

        return (json.JSONDecoder().decode(args['bb_ne']),json.JSONDecoder().decode(args['bb_sw']),args['contents'],args['sea'])

    @cherrypy.expose
    def index(self,**args):
        cherrypy.log('Containers WS is being invoked...')

        targets = []

        cherrypy.log('args: ' + '.'.join(args))
	if 'bb_ne' in args and 'bb_sw' in args:
            cherrypy.log('bb_ne: '+args['bb_ne'])
            cherrypy.log('bb_sw: '+args['bb_sw'])
            bb_ne, bb_sw, contents, sea = self._parse_boundingbox_args(args)
            targets = self._getTargetsBB(bb_ne, bb_sw, contents, sea)
        else:
            targets = self._getShipsLocations(args['contents'])

        return targets
         
