from __future__ import print_function
import xml.etree.ElementTree as ET
import os, re, json
from datetime import datetime, timedelta

CONFIG_FILENAME = "diagnostics-service-config.xml"

# XMLMQTTParser is used to listen to mqtt messages and parse them using config file
class Processor:
    ''' __init__ Takes config file name as parameter.
        Destination directory is assigned here.
        Include local resources in GG configuration.
        Make sure to change permission of resources.'''
    def __init__(self, config_file_name, dest_directory):
        raise NotImplementedError("This is base class please use derived class!")
    
    # Gets trigger Id
    def get_trigger_id(self, measurements):
        trigger_id = 0
        for meas in measurements:
            if "signal" in meas and "diag_trigger" in meas["signal"]:
                if meas["value_bool"] is 1:
                    trigger_id = re.sub('[a-zA-Z,_(),0 ]', "", meas["signal"])

        return int(trigger_id)

    # Checks if mqtt is trigger signals
    def mqtt_is_trigger_signals(self, mqtt_data):
        for item in mqtt_data:
            if "signal_type" in item and item["signal_type"] == "diag_trigger":
                return True
        return False

    # Checks if mqtt is buffered signals
    def mqtt_is_buffer_signals(self, mqtt_data):
        for item in mqtt_data:
            if "signal_type" in item and item["signal_type"] == "diag_code":
                return True
        return False

    # Parse trigger measurements
    def parse_trigger_measurements(self, measurements):
        try:
            parsed_meas = {
                "custom_data": []
            }
            for item in measurements:
                if "signal_type" in item and "diag_trigger" == item["signal_type"]:
                    parsed_meas["index_{}".format(item["diag_index"])] = int(item["value_bool"])
                elif "value_str" in item:
                    parsed_meas["custom_data"].append({
                        "name": item["signal"],
                        "value_str": item["value_str"]
                    })
            parsed_meas["timestamp"] = str(measurements[0]["timestamp"])
            
            return parsed_meas
        except Exception as exc:
            print('Error while parsing trigger measurements method: {}'.format(exc))
            return {}
            
    # Parse buffer measurements
    def parse_buffer_measurements(self, measurements):
        try:
            parsed_meas = {}
            for item in measurements:          
                if item["signal_type"] == "diag_code":
                    event_index = item["diag_index"]
                    event = {                         
                        "timestamp": item["timestamp"],
                        "event_id": item["value_dbl"],
                        "state": "ACTIVE" if event_index == 1 else "PASSIVE",
                        "custom_data": []
                    }
                    parsed_meas[event_index] = event

            for item in measurements:
                if item["signal_type"] == "diag_metadata":
                    event_index = item["diag_index"]                  
                    parsed_meas[event_index]["custom_data"].append({
                        "name": item["signal"],
                        "value_dbl": item["value_dbl"]
                    })
                    
            return parsed_meas
        except Exception as exc:
            print("exception: {}".format(exc))
            return {}

    # append available translations to the event
    def add_translations_to_event(self, event, event_id, translations):
        event_translations = {}    
        keys_to_pop = ['Class', 'ID']
        for language in self.languages:
            if "row_{}".format(event_id) in translations[language]:
                event_translation = translations[language]['row_{}'.format(event_id)]
                for key in keys_to_pop:
                    if key in event_translation:
                        event_translation.pop(key) 
                event_translations[language] = event_translation
        if event_translations:
            event['translations'] = event_translations
        return event
            
    # Gets events for trigger mqtt
    def get_events_for_trigger(self, config_data, measurements, hierarchy_level, serial_number, translations):
        parsed_meas = self.parse_trigger_measurements(measurements)
        latest_record = self.get_latest_trigger_record(serial_number, hierarchy_level)
        duration = 0
        events_to_return = []
        trigger_id = self.get_trigger_id(measurements)

        if latest_record != None:
            time_diff = datetime.strptime(parsed_meas["timestamp"][:-1], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(latest_record["timestamp"][:-1], "%Y-%m-%dT%H:%M:%S.%f")
            diff_ms = (time_diff.seconds * 1000) + (time_diff.microseconds / 1000)
            duration = diff_ms + int(latest_record["duration"])

        # lets append new event as ACTIVE
        event = {
            "timestamp": parsed_meas["timestamp"],
            "state": "ACTIVE",
            "duration_ms": str(duration) if latest_record != None and latest_record["event_id"] == trigger_id else 0,
            "hierarchy_level": hierarchy_level
        }
        if "row_{}".format(trigger_id) in config_data:
            config_row = config_data["row_{}".format(trigger_id)]
            # print( 'Config: {}'.format( json.dumps(config_row) ) )
        else:
            print("Config file does not contain data on event ID {}".format(trigger_id))
            config_row = {
                "id": trigger_id,
                "class": "UNKNOWN",
                "description": "No description found!"
            }
            # print( 'Config: {}'.format( json.dumps(config_row) ) ) 
        for item in config_row:
            event[item.lower()] = config_row[item]
        event["level"] = event.pop("class")
        event["ID"] = event.pop("id")
        if "custom_data" in parsed_meas:
            event["custom_data"] = parsed_meas["custom_data"]
        
        events_to_return.append( self.add_translations_to_event(event, trigger_id, translations) )

        # lets append the existing record as PASSIVE
        if latest_record != None and latest_record["event_id"] != trigger_id:
            old_event = {
                "timestamp": latest_record["timestamp"],
                "duration_ms": str(duration),
                "state": "PASSIVE",
                "hierarchy_level": hierarchy_level
            }
            latest_record_config = config_data["row_{}".format(latest_record["event_id"])]
            for item in latest_record_config:
                old_event[item.lower()] = latest_record_config[item]
            events_to_return.append(old_event)

        if latest_record is None:
            self.put_latest_trigger_record(serial_number, trigger_id, event["timestamp"], hierarchy_level, event["duration_ms"])
        else:
            self.update_latest_trigger_record(serial_number, trigger_id, event["timestamp"], hierarchy_level, event["duration_ms"])
        return events_to_return

    # Gets events for buffer mqtt
    def get_events_for_buffer(self, config_data, measurements, hierarchy_level, serial_number, translations):
        events_to_return = []
        parsed_meas = self.parse_buffer_measurements(measurements)
        latest_record = self.get_latest_buffer_record(serial_number, hierarchy_level)   
        new_record = {}
        hour_counter = None

        for index in parsed_meas:
            event = {}
            item_data = parsed_meas[index]
            event_id = item_data["event_id"]
            event["timestamp"] = item_data["timestamp"]
            event["hierarchy_level"] = hierarchy_level
            event["state"] = item_data["state"]

            if "row_{}".format(event_id) in config_data:
                config_row = config_data["row_{}".format(event_id)]
                # print( 'Config: {}'.format( json.dumps(config_row) ) ) 
            else:
                print("Config file does not contain data on event ID {}".format(event_id))
                config_row = {
                    "id": event_id,
                    "class": "UNKNOWN",
                    "description": "No description found!"
                }
                # print( 'Config: {}'.format( json.dumps(config_row) ) ) 
            for item in config_row:
                event[item.lower()] = config_row[item]
            
            event["level"] = event.pop("class")
            event["ID"] = event.pop("id")
            if "custom_data" in item_data:
                event["custom_data"] = item_data["custom_data"]
                for custom_item in event["custom_data"]:
                    if "Hour counter" in custom_item["name"]:
                        hour_counter = custom_item["value_dbl"]
            
            if index == 1:
                new_record["event_id"] = event_id
                new_record["hour_counter"] = hour_counter
            
            if latest_record != None and event_id == latest_record["event_id"] and hour_counter == latest_record["hour_counter"]:
                break          
            
            events_to_return.append( self.add_translations_to_event(event, event_id, translations) )
        
        if 'event_id' in new_record and 'hour_counter' in new_record:
            if latest_record is None:
                self.put_latest_buffer_record(serial_number, new_record["event_id"], new_record["hour_counter"], hierarchy_level) 
            else:
                self.update_latest_buffer_record(serial_number, new_record["event_id"], new_record["hour_counter"], hierarchy_level)
        else:
            print('unable to update latest_buffer_record, new_record={}'.format(json.dumps(new_record)))        
        return events_to_return

    # Gets events
    def get_events(self, config_data, measurements, hierarchy_level, serial_number, translations):
        if not config_data:
            print("Empty config data - unable to fetch events")
            return []

        if not measurements:
            print("Measurements not found in input data - unable to fetch events.")
            return []
        
        if(self.mqtt_is_buffer_signals(measurements)):
            self.is_mqtt_buffer = True
            return self.get_events_for_buffer(config_data, measurements, hierarchy_level, serial_number, translations)
        
        if(self.mqtt_is_trigger_signals(measurements)):
            self.is_mqtt_trigger = True
            return self.get_events_for_trigger(config_data, measurements, hierarchy_level, serial_number, translations)           
          
    # Get events for subcomponents
    def get_sub_component_events(self, sub_component, config_data, translations):
        sub_component['events'] = self.get_events(config_data, sub_component['measurements'], "sub_component", sub_component["component_serial"], translations)
        sub_component.pop("measurements", None)
        
        if "sub_components" in sub_component:
            for sub_comp in sub_component['sub_components']: 
                return self.get_sub_component_events(sub_comp, config_data, translations)
        return sub_component

    # Gets equipments from mqtt data
    def get_equipment_events(self, config_data, equipments, translations):
        if not config_data or not equipments:
            return []

        equipment_events = equipments
        for equip in equipment_events:
            if "measurements" in equip:
                equip["events"] = self.get_events(config_data, equip["measurements"], "equipment", equip["equipment_serial"], translations)
                equip.pop("measurements", None)

            if "components" in equip:
                for comp in equip["components"]:
                    comp["events"] = self.get_events(config_data, comp["measurements"], "component", comp["component_serial"], translations)
                    comp.pop("measurements", None)
                # if "sub_components" in comp:
                #     for sub_comp in comp['sub_components']:
                #         sub_comp = self.get_sub_component_events(sub_comp, config_data, translations)    

        return equipment_events

    # Reads config file (usually config.xml)
    def read_config_file(self, config=CONFIG_FILENAME):
        try:
            if not os.path.isfile(self.dest_directory + config):
                return None
            with open(os.path.abspath(self.dest_directory + config), 'r') as config_file:
                data = config_file.read()
            root = ET.fromstring(data)
            json_to_return = {}
            for row in root:
                row_name = ''
                row_data = {}
                for child_element in row:
                    row_data[child_element.tag] = child_element.text
                    if child_element.tag == 'ID':
                        row_name = row.tag + "_" + child_element.text
                json_to_return[row_name] = row_data
            return json_to_return
        except Exception as exc:
            return None

    # Gets config data and beautified mqtt data, processes them and returns the processed data
    def process_data(self, config_data, stream_data, translations={}):
        if not config_data:
            raise Exception('Error while processing config data!')

        if not stream_data:
            raise Exception('Error while processing input data!')
    
        processed_data = {
            "version": stream_data["version"],
            "timestamp": stream_data["timestamp"],
            "dcu_type": stream_data["dcu_type"],
            "dcu_serial": stream_data["dcu_serial"],
            "dcu_meta_data": stream_data["dcu_meta_data"],
            "events": self.get_events(config_data, stream_data["measurements"], "top", stream_data["dcu_serial"], translations),
            "equipments": self.get_equipment_events(config_data, stream_data["equipments"], translations)
        }

        return processed_data
