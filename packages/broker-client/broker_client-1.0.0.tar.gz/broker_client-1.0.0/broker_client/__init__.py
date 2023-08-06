# -*- coding: utf-8 -*-

import requests
import json
import logging
import time
from threading import Timer
from functools import wraps
import urllib.parse

from .files import *
from .economy import *
from .consumer import *

from .service import read_description, find_my_ip
from .access_control import read_policies, build_access_request, operations_to_restful_methods

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class BrokerClient():
    def __init__(self, **kwargs):
        logging.info("Initializing BrokerClient with kwargs: %s" % kwargs)

        self.sd, self.sd_filename = {}, ""
        self.policies, self.policies_filename = {}, ""
        self.keys, self.keys_filename = {}, ""

        if "sd" in kwargs.keys():
            self.sd = kwargs["sd"]
        elif "sd_filename" in kwargs.keys():
            self.sd_filename = kwargs["sd_filename"]
            self.sd = read_description(self.sd_filename)

        my_ip = find_my_ip()
        my_id = self.sd["@id"] if "@id" in self.sd else my_ip
        parsed_id = urllib.parse.urlparse(my_id)
        parsed_id._replace(netloc="{}:{}".format(my_ip, parsed_id.port))

        self.sd["@id"] = parsed_id.geturl()
        self.sd["broker"] = "http://" + my_ip + ":4000/broker"
        self.sd["walletId"] = None
        self.sd["@type"] = self.sd["@type"] if "@type" in self.sd else "swarm:BrokerClient"

        if "policies_filename" in kwargs.keys():
            self.policies_filename = kwargs["policies_filename"]
            self.policies = read_policies(self.sd, self.policies_filename)
        if "keys_filename" in kwargs.keys():
            self.keys_filename = kwargs["keys_filename"]
            self.keys = get_keys_and_wallet_id(self.keys_filename)
            self.sd["walletId"] = self.keys["walletId"]

    def register(self):
        registry_url = self.sd["broker"] + "/registry"
        try:
            response = requests.post(registry_url, json=self.sd)
            if response.status_code == 200:
                logging.info("Registered service %s" % (self.sd["@type"]))
                return True
            else:
                logging.error("Error registering service %s: %d" % (self.sd["@type"], response.status_code))
                return False
        except Exception as e:
            logging.debug(e)
            logging.error("No available broker at %s to register at" % registry_url)
            return False

    def setup_default_policies(self):
        policies_url = self.sd["broker"] + "/api/v2/security/policies"
        try:
            response = requests.post(policies_url, json=self.policies)
            policy_names = list(map(lambda p: p["name"], self.policies))
            if response.status_code == 200:
                logging.info("Added policies %s" % (policy_names))
                return True
            else:
                logging.error("Error adding policies %s. Status = %d" % (policy_names, response.status_code))
                return False
        except Exception as e:
            logging.debug(e)
            logging.error("No available broker at %s to add policies" % policies_url)
            return False

    def enforce_authorization(self, f):
        @wraps(f)
        def wrap(*args, **kwargs):
            from flask import request
            access_request = build_access_request(self.sd, request.headers, request.method)
            pdp_url = self.sd["broker"] + "/api/v2/security/authorizations"
            try:
                result = requests.post(pdp_url, json=access_request)
                if result.status_code == 200:
                    logging.debug("Request was authorized: %s" % access_request)
                    return f(*args, **kwargs)
                else:
                    logging.debug("Request was denied: %s" % access_request)
                    return (json.dumps({"error": "access denied", "user_attrs": access_request["user_attrs"]}), 401)
            except Exception as e:
                logging.debug(e)
                return (json.dumps({"error": str(e), "user_attrs": access_request["user_attrs"]}), 400)
        return wrap

    def locate(self, query={"@type": "*"}):
        locate_url = self.sd["broker"] + "/locate-requests"
        try:
            logging.info("Locating query %s" % query)
            response = requests.post(locate_url, json=query)
            services = response.json()
            logging.info("Located services are %s" % list(map(lambda s: s["@id"], services)))
            return services
        except Exception as e:
            logging.debug("The locate request at %s did not work" % locate_url)
            return []

    def update_wallet_id(self, wallet_id):
        self.sd["walletId"] = wallet_id

    def contract(self, data={"query": {"@type": "*"}}):
        contract_url = self.sd["broker"] + "/contracts"
        try:
            logging.info("Running contract for %s" % data)
            response = requests.post(contract_url, json=data)
            location = response.headers['location']
            contract = response.json()
            logging.info("State dict created is %s '\n' And the transaction signed\
                         must be sent to location %s" % (json.dumps(contract),location))
            # return {'contract':contract,'location':location}
            return (contract, location)
        except Exception as e:
            logging.debug("The contract request at %s did not work" % contract_url)
            return None

    # def sign_and_send_tx(self, negotiation):
    def sign_and_send_tx(self, contract, location):
        signed_tx = sign_tx(contract['tx'], self.keys)
        logging.debug("Signed tx: %s" % (signed_tx))
        url = self.sd["broker"] + location
        if signed_tx and location:
            try:
                response = requests.put(url, json={"tx": signed_tx})
                if response.status_code == 200:
                    contract = self.wait_sla_establishment(url)
                    #contract = {'delegate_token':token, "tx": tx, "state": state}
                    logging.info("The negotiation is complete")
                    return contract
            except Exception as e:
                logging.debug(e)
                logging.info("Sending the signed transaction did not work")
                return None
        else:
            logging.error("signed_tx: %s\nlocation: %s" % (signed_tx, location))
            return None

    def wait_sla_establishment(self, url):
        status, max_retries, retries = 0, 3, 0
        block_period = 3
        while status != 200 and retries < max_retries:
            response = requests.get(url)
            status = response.status_code
            retries += 1
            if status != 200:
                time.sleep(block_period)
        if retries <= max_retries:
            return response.json()
        else:
            return None

    def get_provider_sd(self, provider_id):
        provider_ip = urllib.parse.urlparse(provider_id).hostname
        registry_url = "http://" + provider_ip + ":4000/broker/registry/" + urllib.parse.quote(provider_id, safe="")
        logging.debug("Will get provider_id at: %s" % registry_url)
        try:
            response = requests.get(registry_url)
            if response.status_code == 200:
                provider_sd = response.json()
                logging.info("Got provider_id sd: %s" % (provider_sd["@type"]))
                return provider_sd
            else:
                logging.error("Error registering service %s: %d" % (self.sd["@type"], response.status_code))
                return {}
        except Exception as e:
            logging.debug(e)
            logging.error("Could not get provider id at %s" % provider_id)
            return {}

    def smart_use(self, contract, method=None, data=None, token=None):
        provider_id = contract["sla"][0]["provider_id"]
        provider_sd = self.get_provider_sd(provider_id)
        entry = provider_sd["supportedOperations"][0]["entry"]

        operations = contract["tx"]["content"]["operations"]
        if "delegate" not in operations:
            method = operations_to_restful_methods()[operations[0]]

        if method:
            return self.use(method, provider_id + entry, data, token)
        else:
            raise "Could not infer method (%s)" % (method)

    def use(self, method, url, data=None, token=None):
        user_attrs = {"swarm:Id": self.sd["@id"]}
        if token:
            user_attrs["swarm:Token"] = token
        headers = {'x-user-attrs': urllib.parse.urlencode(user_attrs)}

        print(method, url, headers, data)
        response = requests.request(method, url, headers=headers, json=data)
        logging.debug("Request to %s is %s" % (url, response.status_code))
        return response

    def summary(self):
        return {
            "@id": self.sd["@id"],
            "@type": self.sd["@type"],
            "broker": self.sd["broker"],
            "walletId": self.keys["walletId"]
        }
