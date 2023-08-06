# -*- coding: utf-8 -*-
"""Main module.

This module implements a few functions to handle mappings on a wiremock server.
It is meant not to be complete and to be the most transparent possible, 
in contrast with the official wiremock driver. For example there is no
validation of the payloads.

"""

import glob
import os
import sys
import json
import requests
from logzero import logger
from typing import Any, Dict, Union
from .utils import can_connect_to


class ConnectionError(Exception):
    pass


class Wiremock(object):

    def __init__(self, host=None, port=None, url=None, timeout=1):

        if (host and port):
            url="http://{}:{}".format(host,port)
        self.base_url  = "{}/__admin".format(url)
        self.mappings_url = "{}/{}".format(self.base_url, "mappings")
        self.settings_url = "{}/{}".format(self.base_url, "settings")
        self.reset_url    = "{}/{}".format(self.base_url, "reset")
        self.timeout=timeout
        self.headers = {
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
        }

        if ((host and port) and can_connect_to(host, port) == False):
            raise ConnectionError("Error: wiremock server not found")


    def mappings(self):
        """
        retrieves all mappings
        returns the array of mappings found
        """
        r = requests.get(
            self.mappings_url,
            headers=self.headers,
            timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("[mappings]:Error retrieving mappings: {}".format(r.text())) 
            return []
        else:
            res = r.json()
            return res["mappings"]


    def mapping_by_id(self, id):
        r = requests.get(
            "{}/{}".format(self.mappings_url, id),
            headers=self.headers,
            timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("[mapping_by_id]:Error retrieving mapping: {}".format(r.text())) 
            return -1
        else:
            return r.json()


    def mapping_by_url_and_method(self, url, method):
        mappings = self.mappings()
        for mapping in mappings:
            if ((mapping["request"]["url"] == url) and
                (mapping["request"]["method"] == method)):
                return mapping
        return {}


    def mapping_by_request(self, request: dict):
        num_filter_keys = len(request.keys())
        mappings = self.mappings()
        for mapping in mappings:
            count=0
            inter = mapping['request'].keys() & request.keys()
            if ( len(inter) != num_filter_keys):
                continue
            for k in request.keys():
                if (mapping['request'][k] == request[k]):
                    count += 1
            if (count == num_filter_keys):
                return mapping
        return None


    def mapping_by_request_exact_match(self, request: dict):
        num_filter_keys = len(request.keys())
        mappings = self.mappings()
        for mapping in mappings:
            if (mapping['request'] == request):
                return mapping
        return None


    def populate(self, mappings): 
        """ Populate: adds all passed mappings 
            Returns the list of ids of mappings created
        """
        if (isinstance(mappings, list) == False):
            logger.error("[populate]:ERROR: mappings should be a list")
            return -1

        ids = []
        for mapping in mappings:
            ret = self.add_mapping(mapping)
            if (ret != -1):
                ids.append(ret)
            else:
                logger.error("[populate]:ERROR adding a mapping")
                return -1
            
        return ids


    def populate_from_dir(self, dir):
        """ reads all json files in a directory and adds all mappings
            Returns the list of ids of mappings created
            or None in case of errors
        """
        logger.info("populate_from_dir")

        if (not os.path.exists(dir)):
            logger.error("Error: directory {} does not exists".format(dir))
            return None

        ids = []
        for filename in glob.glob(os.path.join(dir, '*.json')):
            logger.info("Importing {}".format(filename))
            with open(filename) as f:
                mapping = json.load(f)
                ids.append(self.add_mapping(mapping))
        return ids


    def update_mapping(self, id: str="", mapping: dict = {}):
        """ updates the mapping pointed by id with new mapping """
        r = requests.put(
                "{}/{}".format(self.mappings_url, id),
                headers=self.headers,
                data=json.dumps(mapping),
                timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("Error updating a mapping: "+r.text)
            return None
        else:
            return r.json()


    def add_mapping(self, mapping: Dict):
        """ add_mapping: add a mapping passed as attribute """
        r = requests.post(
                self.mappings_url,
                headers=self.headers,
                data=json.dumps(mapping),
                timeout=self.timeout)
        if (r.status_code != 201):
            logger.error("Error creating a mapping: "+r.text)
            return -1
        else:
            res = r.json()
            return res['id']
    

    def delete_mapping(self, id: str):
        r = requests.delete(
                "{}/{}".format(self.mappings_url, id),
                timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("Error deleting mapping {}: {}".format(id, r.text))
            return -1
        else:
            return id

    def delete_all_mappings(self):
        mappings = self.mappings()
        for mapping in mappings:
            self.delete_mapping(mapping["id"])
        return len(mappings)


    def fixed_delay(self, request, fixedDelayMilliseconds=0):
        """ 
        updates the mapping adding a fixed delay 
        returns the updated mapping or none in case of errors
        """
        mapping_found = self.mapping_by_request_exact_match(request)

        if ("id" not in mapping_found):
            logger.error("[fixed_delay]: Error retrieving mapping")
            return None

        mapping_found["response"]["fixedDelayMilliseconds"] = fixedDelayMilliseconds
        return self.update_mapping(mapping_found["id"], mapping_found)


    def global_fixed_delay(self, fixedDelay):
        r = requests.post(
                self.settings_url,
                headers=self.headers,
                data=json.dumps({"fixedDelay": fixedDelay}),
                timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("[global_fixed_delay]: Error setting delay: {}".format(r.text))
            return -1
        else:
            return 1
        

    def random_delay(self, filter, delayDistribution):
        """
        Updates the mapping adding a random delay
        returns the updated mapping or none in case of errors
        """
        if ( not isinstance(delayDistribution, dict)):
            logger.error("[random_delay]: parameter has to be a dictionary");

        mapping_found = self.mapping_by_request_exact_match(filter)

        if ("id" not in mapping_found):
            logger.error("[fixed_delay]: Error retrieving mapping")
            return None

        mapping_found["response"]["delayDistribution"] = delayDistribution
        return self.update_mapping(mapping_found["id"], mapping_found)

    def global_random_delay(self, delayDistribution):
        if ( not isinstance(delayDistribution, dict)):
            logger.error("[global_random_delay]: parameter has to be a dictionary");
        r = requests.post(
                self.settings_url,
                headers=self.headers,
                data=json.dumps({"delayDistribution": delayDistribution}),
                timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("[global_random_delay]: Error setting delay: {}".format(r.text))
            return -1
        else:
            return 1

    def chunked_dribble_delay(self, filter, chunkedDribbleDelay):
        """
        Adds a delay to the passed mapping
        returns the updated mapping or non in case of errors
        """
        if ( not isinstance(chunkedDribbleDelay, dict)):
            logger.error("[chunked_dribble_delay]: parameter has to be a dictionary");
        if ( "numberOfChunks" not in chunkedDribbleDelay ):
            logger.error("chunked_dribble_delay]: attribute numberOfChunks not found in parameter")
            return None
        if ( "totalDuration" not in chunkedDribbleDelay ):
            logger.error("chunked_dribble_delay]: attribute totalDuration not found in parameter")
            return None

        mapping_found = self.mapping_by_request_exact_match(filter)

        if ("id" not in mapping_found):
            logger.error("[chunked_dribble_delay]: Error retrieving mapping")
            return None

        mapping_found["response"]["chunkedDribbleDelay"] = chunkedDribbleDelay
        return self.update_mapping(mapping_found["id"], mapping_found)

    def up(self, filter: list=[]):
        """ resets a list of mappings deleting all delays attached to them """
        ids = []
        for f in filter:
            mapping_found = self.mapping_by_request_exact_match(f)
            if (not mapping_found):
                next
            else:
                logger.debug("[up]: found mapping: {}".format(mapping_found["id"]))
                for key in ['fixedDelayMilliseconds', 'delayDistribution', 'chunkedDribbleDelay']:
                    if (key in mapping_found["response"]): del mapping_found["response"][key]
                self.update_mapping(mapping_found["id"], mapping_found)
        return ids


    def reset(self):
        r = requests.post(
                self.reset_url,
                headers=self.headers,
                timeout=self.timeout)
        if (r.status_code != 200):
            logger.error("Error resetting wiremock server "+r.text)
            return -1
        else:
            return 1
