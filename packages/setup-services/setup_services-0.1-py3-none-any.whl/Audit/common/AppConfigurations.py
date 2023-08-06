import configparser
from upload import __root__
import json
import os
import ast

#Root path
root_path = __root__.path()

# Properties file
CONFIGURATION_FILE = "conf\settings.conf"

# Config file parser
parser = configparser.RawConfigParser()

parser.read(CONFIGURATION_FILE)

# Log
# LOG_BASE_PATH = parser.get('LOG', 'base_path')
LOG_LEVEL = parser.get('LOG', 'log_level')
LOG_BASEPATH = os.environ.get('LOG_BASEPATH', parser.get('LOG', 'basepath', fallback="logs/"))
FILE_NAME = LOG_BASEPATH + os.environ.get('FILE_NAME', parser.get('LOG', 'file_name', fallback="audit-services"))
FILE_NAME_JSON = LOG_BASEPATH + os.environ.get('FILE_NAME_JSON',
                                               parser.get('LOG', 'file_name_json', fallback="file_name_json"))
LOG_HANDLERS = os.environ.get('LOG_HANDLERS',
                              parser.get('LOG', 'handlers', fallback='["file", "jsonFile", "console"]'))

# Adaptors
persistence_adaptor = parser.get('ADAPTOR', 'persistence_adaptor')

# Server
PORT = os.environ.get('SERVICE_PORT', parser.get('SERVER', 'port', fallback=17223))