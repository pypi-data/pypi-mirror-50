from __future__ import print_function
import json
from cloud_processor import CloudProcessor

LANGUAGES = 'de,es,fr,it,pt'
CONFIG_FILENAME = 'diagnostics-service-config.xml'
RESOURCE_DESTINATION = './resources/'
CONFIG_FILENAME_PREFIX = 'diagnostics-service-config'



def compute(message):
  languages = LANGUAGES.split(',')
  processor = CloudProcessor(CONFIG_FILENAME, RESOURCE_DESTINATION, languages)
  config_data = processor.read_config_file()
  
  # read config for different languages
  translations = {}
  for language in languages:
    config_name = '{}-{}.xml'.format( CONFIG_FILENAME_PREFIX, language )
    translations[language] = processor.read_config_file(config_name)

  data = message
  if isinstance(data, str):
    data = json.loads(data)
  processed_data = processor.process_data(config_data, data, translations)
  return json.dumps( processed_data )

if __name__ == '__main__':
  compute()