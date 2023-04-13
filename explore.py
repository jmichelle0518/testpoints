import requests
import json
import pandas as pd

response_API = requests.get('https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/5/query?outFields=*&where=1%3D1&f=geojson')
# print(response_API.status_code)
data = response_API.text
parse_json = json.loads(data)

df = pd.json_normalize(parse_json, record_path = ['features'])
df.set_index('id',inplace=True)
column_heads = {
    'type': 'type',
    'geometry.type': 'GEO_TYPE',
    'geometry.coordinates': 'COORDINATES',
    'properties.SHIFT': 'SHIFT',
    'properties.METHOD': 'METHOD',
    'properties.OFFENSE': 'OFFENSE',
    'properties.BLOCK': 'BLOCK',
    'properties.XBLOCK': 'XBLOCK',
    'properties.YBLOCK': 'YBLOCK',
    'properties.WARD': 'WARD',
    'properties.ANC': 'ANC',
    'properties.DISTRICT': 'DISTRICT',
    'properties.PSA': 'PSA',
    'properties.NEIGHBORHOOD_CLUSTER': 'NEIGHBORHOOD_CLUSTER',
    'properties.BLOCK_GROUP': 'BLOCK_GROUP',
    'properties.CENSUS_TRACT': 'CENSUS_TRACT',
    'properties.VOTING_PRECINCT': 'VOTING_PRECINCT',
    'properties.LATITUDE': 'LATITUDE',
    'properties.LONGITUDE': 'LONGITUDE',
    'properties.BID': 'BID',
    'properties.REPORT_DAT': 'REPORT_DATE',
    'properties.START_DATE': 'START_DATE',
    'properties.END_DATE': 'END_DATE',
}

df.rename(column_heads,axis='columns',inplace=True)
df['REPORT_DATE']=pd.to_datetime(df['REPORT_DATE'],origin='unix',unit='ms')
df['START_DATE'] = pd.to_datetime(df['START_DATE'],origin='unix',unit='ms')
df['END_DATE'] = pd.to_datetime(df['END_DATE'],origin='unix',unit='ms')
df = df.drop(['properties.CCN','type','properties.OBJECTID','properties.OCTO_RECORD_ID'],axis=1)

#print(parse_json['features'])
#print(df)
#print(df['properties.START_DATE'].describe)
#print()
#print(df.info(verbose=True))
print(df.value_counts(subset=['SHIFT','METHOD']))

df_sub = df.sample(n=4)
print(df_sub)

df_change = df[df["SHIFT"].shift() != df["SHIFT"]]
#print(df_change)


df_offenses = df.groupby(['OFFENSE','METHOD']).count()
print(df_offenses)
df_offenses.plot.bar