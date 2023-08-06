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

This is the main PyDrake class containing the core functions of the API
"""
import requests

from .summonerv4 import Summoner
from .leaguev4 import RankedSummoner
from .matchv4 import MatchList, Match
from .errors import APIError
from .ddragon import *

# Supported rate_limit_mode values
supported_modes = ["off", "soft", "hard"]
# Supported regions for API requests
supported_regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na", "na1", "oc1", "tr1", "ru", "pbe1"]

# Base URL for the Riot Games API
BASE_URL = "https://{}.api.riotgames.com/lol/"


class PyDrake:
    def __init__(self, api_key, rate_limit_mode="off"):
        """
        PyDrake is the main API wrapper class that will be used to call all
        Riot Games API functions
        :param api_key: Your Riot Games API Key
        :param rate_limit_mode: The rate-limiting mode to use
            Can be set to:
                - "off": default value, use no client-side rate-limiting
                - "soft": PyDrake will attempt to execute a request, on receiving a
                        429 response code it will wait the amount of time specified
                        in the Retry-After response header
                - "hard": PyDrake will raise an APIError on receiving a 429
                        response code
        """
        self.api_key = api_key
        if rate_limit_mode.lower() in supported_modes:
            self.rate_limit_mode = rate_limit_mode
        else:
            raise ValueError("{} is not a valid rate_limit_mode argument".format(rate_limit_mode))

    def _call_api(self, region, extension):
        """
        Returns a JSON response object from the Riot Games API.
        This function should only be used internally.
        :param region: The region code of the API server to use. A ValueError
                    will be thrown if this is an invalid region code
        :param extension: The URL extension to use for the API request
        :return: dict (JSON response data)
        """
        if region.lower() not in supported_regions:
            raise ValueError("{} is not a supported service region".format(region.lower()))

        try:
            r = requests.get(BASE_URL.format(region.lower()) + extension, params={"api_key": self.api_key})
        except requests.exceptions.ConnectionError as e:
            raise APIError(str(e))

        if r.status_code != 200:
            if r.status_code == 401:
                raise APIError("401 Unauthorized: Your API key may be invalid")
            elif r.status_code == 403:
                raise APIError("403 Forbidden: The endpoint you tried to reach may not exist")
            elif r.status_code == 404:
                raise APIError("404 Not Found: {}".format(r.json()['status']['message']))
            elif r.status_code == 429:
                # TODO: Rate-limiting logic
                pass
        else:
            return r.json()

    @property
    def get_champion_by_id(self):
        """
        Wrapper function for Data Dragon
        """
        return get_champion_by_id

    def get_summoner_by_name(self, name, region):
        """
        Retrieve statistics about a summoner by their name. Returns a Summoner
        object with all information retrieved from the API
        :param name: The name of the summoner to retrieve
        :param region: The region code that the account belongs to
        :return: A Summoner object
        """
        response = self._call_api(region, "summoner/v4/summoners/by-name/{}".format(name))
        return Summoner(response, region)

    def get_ranked_summoner(self, summoner):
        """
        Retrieves the ranking information for the given summoner and returns a
        RankedSummoner object containing the new information
        :param summoner:
        :return: A RankedSummoner object
        """
        response = self._call_api(summoner.region, "league/v4/entries/by-summoner/{}".format(summoner.id))
        return RankedSummoner(response, summoner)

    def get_summoner_matchlist(self, summoner):
        """
        Retrieves the matchlist for the given summoner
        :param summoner: The summoner to retrieve match data for
        :return: A MatchList object
        """
        response = self._call_api(summoner.region, "match/v4/matchlists/by-account/{}".format(summoner.account_id))
        return MatchList(response)

    def get_match_from_matchlist(self, match):
        """
        Retrieves the full data for a match from an item in a MatchList object
        :param match: The MatchListMatch object to retrieve further data for
        :return: a Match object containing all of the data about the match
        """
        response = self._call_api(match.platform_id, "match/v4/matches/{}".format(match.game_id))
        return Match(response)
