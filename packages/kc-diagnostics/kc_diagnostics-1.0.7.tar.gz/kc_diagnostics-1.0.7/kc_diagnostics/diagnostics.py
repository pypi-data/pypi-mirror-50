from __future__ import print_function
import json
from cloud_processor import CloudProcessor

LANGUAGES = 'de,es,fr,it,pt'
CONFIG_FILENAME = 'diagnostics-service-config.xml'
RESOURCE_DESTINATION = './kc_diagnostics/resources/'
CONFIG_FILENAME_PREFIX = 'diagnostics-service-config'


class Diagnostics():
  def __init__(self):
    self.languages = LANGUAGES.split(',')
    self.processor = CloudProcessor(CONFIG_FILENAME, RESOURCE_DESTINATION, self.languages)
    self.config_data = self.processor.read_config_file(CONFIG_FILENAME)
    self.translations = self.load_translations()

  def load_translations(self):
    translations = {}
    for language in self.languages:
      config_name = '{}-{}.xml'.format( CONFIG_FILENAME_PREFIX, language )
      translations[language] = self.processor.read_config_file(config_name)
    return translations
  
  def generate_alerts(self, data):
    if isinstance(data, str):
      data = json.loads(data)
    
    processed_data = self.processor.process_data(self.config_data, data, self.translations)
    return json.dumps( processed_data )    



if __name__ == '__main__':
  diag = Diagnostics()
  diag.generate_alerts({})