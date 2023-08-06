# Controller Logic

import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('api-config.ini')


class Dome9SG:

    def __init__(self, **kwargs):

        """ Initialising configuration """

        self.api_url = config['api']['apiURL']
        self.headers = {'Accept': 'application/json'}
        self.api_secret = config['api']['apiSecret']
        self.api_key = config['api']['apiKey']
        self.aws_dome9map = config['aws-dome9-map']
        self.sg_id = kwargs.get('sg_id', None)
        self.sg_name = kwargs.get('sg_name', None)
        self.ac_id = kwargs.get('ac_id', None)
        self.region_id = kwargs.get('region_id', None)

    def get_sg_by_id(self):

        """ Fetch single SG details as provided by SOC Team """

        url_2 = self.api_url + "/cloudsecuritygroup/" + self.sg_id
        result = requests.get(url_2, headers=self.headers, auth=(self.api_key, self.api_secret))
        if result.status_code != 200:
            return {"Result": "Not found..."}
        return result.json()

    def get_all_sg_by_name(self):

        """ Fetch all SG details by name associated with Dome9 """

        url_2 = self.api_url + "/cloudsecuritygroup"
        result = requests.get(url_2, headers=self.headers, auth=(self.api_key, self.api_secret))
        match_sgs = list()
        if result.status_code != 200:
            return {"Result": "Not found..."}
        else:
            json_re = result.json()
            for item in json_re:
                if item["securityGroupName"] == self.sg_name:
                    match_sgs.append(item)
        return match_sgs

