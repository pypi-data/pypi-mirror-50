##                          _       _
##__      _____  __ ___   ___  __ _| |_ ___
##\ \ /\ / / _ \/ _` \ \ / / |/ _` | __/ _ \
## \ V  V /  __/ (_| |\ V /| | (_| | ||  __/
##  \_/\_/ \___|\__,_| \_/ |_|\__,_|\__\___|
##
## Copyright © 2016 - 2018 Weaviate. All rights reserved.
## LICENSE: https://github.com/creativesoftwarefdn/weaviate/blob/develop/LICENSE.md
## AUTHOR: Bob van Luijt (bob@kub.design)
## See www.creativesoftwarefdn.org for details
## Contact: @CreativeSofwFdn / bob@kub.design
##

"""This module handles the communication with Weaviate."""
import urllib
import json
import requests
from modules.Messages import Messages
from modules.Init import Init
import datetime, time

class Weaviate:
    """This class handles the communication with Weaviate."""

    def __init__(self, c):
        """This function inits the class."""

        # make the config available in this class
        from modules.Helpers import Helpers
        self.config = c
        self.helpers = Helpers

    def GetEpochTime(self):
        dts = datetime.datetime.utcnow()
        return round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)

    def getHeadersForRequest(self, shouldAuthenticate):
        """Returns the correct headers for a request"""

        headers = {"content-type": "application/json"}
        # status, _ = self.Get("/.well-known/openid-configuration")

        # Add bearer if OAuth
        # if status == 200:
        if shouldAuthenticate == True:
            headers["Authorization"] = "Bearer " + self.config["auth_bearer"]

        return headers

    def AuthGetBearer(self):

        # collect data for the request
        try:
            request = requests.get(self.config['url'] + "/weaviate/v1/.well-known/openid-configuration", headers={"content-type": "application/json"})
        except urllib.error.HTTPError as error:
            Helpers(None).Error(Messages().Get(210))  
        if request.status_code != 200:
            Helpers(None).Error(Messages().Get(210))

        # Set the client ID
        clientId = request.json()['clientId']

        # request additional information
        try:
            requestThirdParth = requests.get(request.json()['href'], headers={"content-type": "application/json"})
        except urllib.error.HTTPError as error:
            Helpers(None).Error(Messages().Get(219))
        if requestThirdParth.status_code != 200:
            Helpers(None).Error(Messages().Get(219))

        # Validate third part auth info
        if 'client_credentials' not in requestThirdParth.json()['grant_types_supported']:
            Helpers(None).Error(Messages().Get(220))

        # Set the body
        requestBody = {
            "client_id": clientId,
            "grant_type": 'client_credentials',
            "client_secret": self.config['auth_clientsecret']
        }

        # try the request
        try:
            request = requests.post(requestThirdParth.json()['token_endpoint'], requestBody)
        except urllib.error.HTTPError as error:
            self.helpers(self.config).Error(Messages().Get(216))

        # sleep to process
        time.sleep(4)

        # Update the config file
        Init().UpdateConfigFile('auth_bearer', request.json()['access_token'])
        Init().UpdateConfigFile('auth_expires', int(self.GetEpochTime() + request.json()['expires_in'] - 2))


    def Auth(self):
        """Returns true if one should authenticate"""

        # try to make the well known request
        try:
            request = requests.get(self.config["url"] + "/weaviate/v1/.well-known/openid-configuration", headers=self.getHeadersForRequest(False))
        except urllib.error.HTTPError as error:
            return False

        if request.status_code == 200:
            if (self.config['auth_expires'] - 2) < self.GetEpochTime(): # -2 for some lagtime
                self.helpers(self.config).Info(Messages().Get(141))
                self.AuthGetBearer()
            
            return True

        return False

    def Ping(self):
        """This function pings a Weaviate to see if it is online."""

        self.helpers(self.config).Info("Ping Weaviate...")

        # get the meta endpoint
        try:
            status, _ = self.Get("/meta")
        except:
            self.helpers(self.config).Error(Messages().Get(210))
        # throw error if failed
        if status != 200 or status == None:
            self.helpers(self.config).Error(Messages().Get(210))
        # would fail is not available.
        self.helpers(self.config).Info("Pong from Weaviate...")

    def Delete(self, path):
        """This function deletes from a Weaviate."""

        # Authenticate
        self.Auth()

        # try to request
        try:
            request = requests.delete(self.config["url"] + "/weaviate/v1" + path, headers=self.getHeadersForRequest())
        except urllib.error.HTTPError as error:
            return None

        return request.status_code

    def Post(self, path, body):
        """This function posts to a Weaviate."""

        # Authenticate
        self.Auth()

        # try to request
        try:
            request = requests.post(self.config["url"] + "/weaviate/v1" + path, json.dumps(body), headers=self.getHeadersForRequest())
        except urllib.error.HTTPError as error:
            return 0, json.loads(error.read().decode('utf-8'))

        # return the values
        if len(request.json()) == 0:
            return request.status_code, {}
        else: 
            return request.status_code, request.json()

    def Get(self, path):
        """This function GETS from a Weaviate Weaviate."""

        shouldAuthenticate = self.Auth()

        # try to request
        try:
            request = requests.get(self.config["url"] + "/weaviate/v1" + path, headers=self.getHeadersForRequest(shouldAuthenticate))
        except urllib.error.HTTPError as error:
            return None, json.loads(error.read().decode('utf-8'))

        return request.status_code, request.json()