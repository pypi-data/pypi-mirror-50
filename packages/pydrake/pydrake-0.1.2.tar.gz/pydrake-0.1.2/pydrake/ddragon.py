"""
   Copyright 2019 Jacob Padley

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

This file provides means of accessing Riot's Data Dragon API to retrieve static
data files
"""
from .errors import APIError

import requests

ddragon_base = "http://ddragon.leagueoflegends.com/cdn/9.15.1/data/en_US/"


def get_static_data(extension):
    """
    Retrieves a JSON file from DataDragon
    :param extension: The filename to access
    :return: The JSON data of the file
    """
    # TODO: Smart Caching

    r = requests.get(ddragon_base + extension)
    if r.status_code != 200:
        if r.status_code == 404:
            raise APIError("404 Not Found - The file '{}' doesn't seem to exist".format(extension))
        elif r.status_code == 403:
            raise APIError("403 Forbidden - The file '{}' may not exist or may have been moved".format(extension))
    else:
        return r.json()


class Champion:
    def __init__(self, data):
        """
        Encapsulates information about a Champion from Data Dragon
        :param data: the raw JSON data associated with the champion
        """
        self.id = data['key']
        self.name = data['name']
        self.title = data['title']
        self.blurb = data['blurb']
        self.info = data['info']
        self.tags = data['tags']
        self.image = data['image']
        self.stats = data['stats']


def get_champion_by_id(id):
    """
    Retrieves a Champion object with the given id
    :param id: the ID of the champion. Raises a ValueError if none are found
    :return: a Champion object with the given ID
    """
    raw = get_static_data("champion.json")
    champion_raw = next((x for x in raw['data'].values() if x['key'] == str(id)), None)
    if champion_raw is None:
        raise ValueError("No champion found with ID: {}".format(id))

    return Champion(champion_raw)
