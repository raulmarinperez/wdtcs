# GLOBAL SETTINGS
# ====== ========

# Connection to MongoDB
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'WDTCS'

RESOURCE_METHODS = ['GET','POST']
ITEM_METHODS = ['GET','PATCH','PUT','DELETE']
XML = False
CACHE_CONTROL='max-age=0,must-revalidate'

# BUSINESS ENTITIES
# ======== ========
# See also:
#   - http://python-eve.org/config.html#schema-definition

# Ships definition
#
ships_schema = {
  'Built': {'type':'integer'},
  'Name': {'type':'string'},
  'Length overall (m)': {'type':'number'},
  'Beam (m)': {'type':'number'},
  'Maximum TEU': {'type':'integer'},
  'GT': {'type':'integer'},
  'Owner': {'type':'string'},
  'Country': {'type':'string'},
  'route': { 
    'type': 'dict',
    'schema': {
      'origin': {
        'type': 'dict',
        'schema': {
          'Name': {'type':'string'},
          'Country': {'type':'string'} } },
      'destination': {
        'type': 'dict',
        'schema': {
          'Name': {'type':'string'},
          'Country': {'type':'string'} } } } },
  'location': {'type': 'point'},
  'EAT': {'type':'datetime'}
}

ships = {
  'item_title': 'ship',
  'schema': ships_schema
}

# Ports definition
#
ports_schema = {
  'Ranking': {'type':'integer'},
  'Name': {'type':'string'},
  'Country': {'type':'string'} 
}

ports = {
  'item_title': 'port',
  'schema': ports_schema
}

# Containers definition
#
containers_schema = {
  'container_id': {'type':'string'},
  'type': {'type':'string'},
  'shipName': {'type':'string'},
  'cargo': {'type':'string'},
  'Tons': {'type':'integer'},
  'location': {'type':'point'}
}

containers = {
  'item_title': 'container',
  'schema': containers_schema
}

# Countries definition
#
countries_schema = {
  'type': {'type':'string'},
  'properties': {
    'type': 'dict',
    'schema': {
      'scalerank': {'type':'integer'},
      'featurecla': {'type':'string'},
      'labelrank': {'type':'integer'},
      'sovereignt': {'type':'string'},
      'sov_a3': {'type':'string'},
      'adm0_dif': {'type':'integer'},
      'level': {'type':'integer'},
      'type': {'type':'string'},
      'admin': {'type':'string'},
      'adm0_a3': {'type':'string'},
      'geou_dif': {'type':'integer'},
      'geounit': {'type':'string'},
      'gu_a3': {'type':'string'},
      'su_dif': {'type':'integer'},
      'subunit': {'type':'string'},
      'su_a3': {'type':'string'},
      'name': {'type':'string'},
      'name_long': {'type':'string'},
      'brk_a3': {'type':'string'},
      'brk_name': {'type':'string'},
      'brk_group': {'type':'string'},
      'abbrev': {'type':'string'},
      'postal': {'type':'string'},
      'formal_en': {'type':'string'},
      'formal_fr': {'type':'string'},
      'note_adm0': {'type':'string'},
      'note_brk': {'type':'string'},
      'name_sort': {'type':'string'},
      'name_alt': {'type':'string'},
      'mapcolor7': {'type':'integer'},
      'mapcolor8': {'type':'integer'},
      'mapcolor9': {'type':'integer'},
      'mapcolor13': {'type':'integer'},
      'pop_est': {'type':'integer'},
      'gdp_md_est': {'type':'integer'},
      'pop_year': {'type':'integer'},
      'lastcensus': {'type':'integer'},
      'economy': {'type':'string'},
      'income_grp': {'type':'string'},
      'wikipedia': {'type':'integer'},
      'fips_10': {'type':'string'},
      'iso_a2': {'type':'string'},
      'iso_a3': {'type':'string'},
      'iso_n3': {'type':'string'},
      'un_a3': {'type':'string'},
      'wb_a2': {'type':'string'},
      'wb_a3': {'type':'string'},
      'woe_id': {'type':'integer'},
      'adm0_a3_is': {'type':'string'},
      'adm0_a3_us': {'type':'string'},
      'adm0_a3_un': {'type':'integer'},
      'adm0_a3_wb': {'type':'integer'},
      'continent': {'type':'string'},
      'region_un': {'type':'string'},
      'subregion': {'type':'string'},
      'region_wb': {'type':'string'},
      'name_len': {'type':'integer'},
      'long_len': {'type':'integer'},
      'abbrev_len': {'type':'integer'},
      'tiny': {'type':'integer'},
      'homepart': {'type':'integer'} } },
   'geometry': {'type':'polygon'}
}

countries = {
  'item_title': 'country',
  'schema': countries_schema
}

# Oceans definition
#
oceans_schema = {
  'type': {'type':'string'},
  'name': {'type':'string'},
  'geometry': {'type':'polygon'}
}

oceans = {
  'item_title': 'ocean',
  'schema': oceans_schema
}

# application's domain
DOMAIN = {
  'ships': ships,
  'ports': ports,
  'containers': containers,
  'countries': countries,
  'oceans': oceans
}
