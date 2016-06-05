import cherrypy
import json
from pymongo import MongoClient

class Containers(object):
    def __init__(self):
        self.client = MongoClient()
        self.ships = self.client['WDTCS']['ships']
        self.containers = self.client['WDTCS']['containers']
        self.oceans = self.client['WDTCS']['oceans']

    def _getTargetsBB(self, bb_ne, bb_sw, contents, sea):
        cherrypy.log('Retrieving ships'' locations by bounding box and contents.')

        matchStage = {'$match' :{'location' : {'$geoWithin' : self._getGeoWithin(bb_ne, bb_sw, sea)}}}
        lookup = {'$lookup' : {'from': "containers", 'as': "cargo", 'localField': "Name", 'foreignField': "shipName"}}
        unwind = {'$unwind': "$cargo"}
        matchStage2 = {'$match' : {'cargo.cargo' : { '$in' : contents.split(',') } } }
        cherrypy.log('matchStage2: ' + contents)
        group = {'$group' : {'_id': {'ship': "$Name", 'cargo' : "$cargo.cargo", 'route': "$route", 'location': "$location"}, 'sum': {'$sum': "$cargo.Tons"}}}
        project = {'$project': {'_id' : {'ship': "$_id.ship", 'route': "$_id.route", 'location': "$_id.location"}, 'cargo' : {'type' : "$_id.cargo", 'Tons': "$sum"}}}
        group2 = {'$group' : {'_id': "$_id", 'cargo': {'$push': "$cargo"}}}
        sort = {'$sort' : {'_id.ship': 1 }}

        if contents!='':
            pipeline = [ matchStage, lookup, unwind, matchStage2, group, project, group2, sort ]
        else:
            pipeline = [ matchStage, lookup, unwind, group, project, group2, sort ]

        ships = list(self.ships.aggregate(pipeline))

        cherrypy.log('Ships numbers: ' + str(len(ships)))
        return json.dumps(ships)

    def _getGeoWithin(self, bb_ne, bb_sw, sea):
        if sea=='':
            return {'$box' : [bb_sw,bb_ne]}

        return {'$geometry' : self._getSeaGeometry(sea) }

    def _getSeaGeometry(self, sea):
        sea_dict = { 'Biscay': 'Bay of Biscay',
                     'Medi': 'Mediterranean Sea',
                     'North': 'NORTH ATLANTIC OCEAN',
                     'Caribbean': 'Caribbean  Sea' }
        return self.oceans.find_one({'name':sea_dict[sea]})['geometry']

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

        return targets
         
