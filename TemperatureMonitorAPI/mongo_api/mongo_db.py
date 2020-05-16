"""
# todo: make fields configurable and parse them using dictionary
# todo: implement different approach to timeout -> assert loading data size in 10 minutes and limit.
"""
import json
import logging
import os
import random

from pymongo import MongoClient

import util_functions


class MongoDatabase(MongoClient):
    def __init__(self, data=None, uri='mongodb://localhost:27017', db_name='temperature_montior_app',
                 log_name='mongo_log'):
        super(MongoDatabase, self).__init__()
        util_functions.init_logger(logger_name=log_name)
        self.logger = logging.getLogger(log_name)
        self.client = MongoClient(uri)
        self.data = data
        self.db = self.client[db_name]
        # self.converted = False
        # self.convert_to_mongodb()

    def insert_new_client(self, data=None):
        if data is not None:
            data_as_json = json.dumps(data)
            self.db.clients.insert_many(data_as_json)
        else:
            self.logger.warning('Data Is Empty!')

    def get_client_by_id(self, client_id, col_name='clients'):
        col = self.db.get_collection(col_name)
        return json.dumps(col.find({"_id": client_id})[0])

    def get_all_clients(self, col_name='clients'):
        col = self.db.get_collection(col_name)
        return json.dumps(col)

    def convert_to_mongodb(self):
        """
        This function converts any supported DB type (currently only Nessus) to a Mongo database.
        :return: updates db object to contain the Nessus data.
        """
        if not self.converted:
            self.logger.info('Starting conversion from {} DB to MongoDB'
                             .format(self.converted_db_type))
            if self.converted_db_type == 'nessus':
                parsed_data = util_functions.parse_json(self.ness_db_data_path)
            else:
                self.logger.error('DB Type is not supported!')
                return
            # posts = self.db.posts
            self.db.posts.insert_many(parsed_data)
            self.logger.info('Done converting {}DB to mongoDB'
                             .format(self.converted_db_type))
            self.converted = True
        else:
            return self.db.posts

    def find_all(self, out_file_path, out_file_name, collection_name='posts'):
        """
        This function gets all plugins from the MongoDB along with certain fields into a JSON
        formatted string.
        :param out_file_path:
        :param out_file_name:
        :param collection_name:
        :return: return the file path where data was saved.
        """
        col = self.db.get_collection(collection_name)
        parsed_json_file_path = os.path.join(out_file_path, out_file_name)
        try:
            with open(parsed_json_file_path, 'w') as outfile:
                for plugin in col.find({}, {"_source.pluginID": 1,
                                            "_source.enchantments.score.value": 1,  # "_score": 1,
                                            "_source.published": 1,
                                            "_source.title": 1,
                                            "_source.cvelist": 1}, no_cursor_timeout=True):
                    plugin_as_str = json.dumps(plugin)
                    json.dump(plugin_as_str, outfile, separators=(',', ': '))
            return parsed_json_file_path
        except Exception as e:
            self.logger.warning('Error occurred! details: {}'.format(e.__str__()))