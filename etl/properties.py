from configparser import ConfigParser
import glob
import os
from cx_Oracle import makedsn

ROOT = os.path.abspath(os.path.dirname(__file__))
RESOURCES = os.path.join(ROOT, 'conf')
_config = ConfigParser()
_files = glob.glob(f'{RESOURCES}/*.ini')
_reports = os.path.join(ROOT, 'data/reports')

csv_dir = os.path.join(_reports, 'csv')

_config.read(_files)
_chunk_size = 20

def get_properties(section:str):
    if section in _config.sections():
        properties = dict(_config[section])
    else:
        raise ValueError(f'Section: {section}, not in properties')
    return properties

def get_oracle_properties(section:str):
    info = {}
    temp = get_properties(section)
    if temp ['sid']== '' and temp['service_name'] == '':
        raise ValueError('sid or service_name must be specified')
    if temp['sid'] is '':
        temp.pop('sid')
    if temp['service_name'] is '':
        temp.pop('service_name')
    connection_details = {'user':temp.pop('user'), 'password': temp.pop('password'), 'dsn': makedsn(**temp)}
    return  connection_details



